import struct

class SHA1(object):

    # Static Variables
    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    k = [0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xCA62C1D6]

    # Constructor
    def __init__(self):
        self._message = b""
        self._cached_hash = None

    def __str__(self):
        self.hash()
        return '{:08x}{:08x}{:08x}{:08x}{:08x}'.format(self._cached_hash[0],self._cached_hash[1],self._cached_hash[2],self._cached_hash[3],self._cached_hash[4])

    def __repr__(self): return struct.pack('>5L', self.hash())

    @staticmethod
    def pad(padded_msg:bytes):
        # Pre-processing: Padding the message
        length = len(padded_msg) * 8
        padded_msg += b'\x80'
        while (len(padded_msg) + 8) % 64 != 0:
            padded_msg += b'\x00'
        padded_msg += struct.pack('>Q', length)
        return padded_msg

    @staticmethod
    def f(loop_number:int, h:list):
        if loop_number < 0 : raise ValueError("loop number must be a positive non-zero integer")
        if len(h) != 3 : raise IndexError(f"h must be an array of 4 values, but {len(h)} was given.")
        b, c ,d = h
        if   loop_number % 80 < 20: return (h[0] & h[1]) | ((~h[0]) & h[2])
        elif loop_number % 80 < 40: return  h[0] ^ h[1] ^ h[2]
        elif loop_number % 80 < 60: return (h[0] & h[1]) | (h[0] & h[2]) | (h[1] & h[2])
        else: return h[0] ^ h[1] ^ h[2]


    @staticmethod
    def round(loop_number:int, h:list, word:int) -> list:
        temp = ((h[0] << 5 | h[0] >> 27)) + SHA1.f(loop_number,h[1:4]) + h[4] + SHA1.k[int(loop_number/20)%4] + word & 0xFFFFFFFF
        h[4] = h[3]
        h[3] = h[2]
        h[2] = (h[1] << 30 | h[1] >> 2)
        h[1] = h[0]
        h[0] = temp
        return h

    def load(self, text:str) -> bool:
        self._message = text.encode()
        self._cached_hash = None
        return True

    def hash(self, rounds:int=80) -> list:
        if self._cached_hash != None :
            h0, h1, h2, h3, h4 = self._cached_hash
        else:
            # Pre-processing: Padding the message
            message = self.pad(self._message)

            # Main loop
            for i in range(0, len(message), 64):
                chunk = message[i:i + 64]
                words = list(struct.unpack('!16L', chunk))
                # message scheduler
                for j in range(16, rounds):
                    words.append(words[j-3] ^ words[j-8] ^ words[j-14] ^ words[j-16])
                    words[j] = (words[j] << 1 | words[j] >> 31) & 0xFFFFFFFF
                # compression rounds
                h0, h1, h2, h3, h4 = self.h
                for j in range(rounds):
                    h0, h1, h2, h3, h4 = self.round(j,[h0,h1,h2,h3,h4],words[j])
                # final addition
                h0 = (self.h[0] + h0) & 0xFFFFFFFF
                h1 = (self.h[1] + h1) & 0xFFFFFFFF
                h2 = (self.h[2] + h2) & 0xFFFFFFFF
                h3 = (self.h[3] + h3) & 0xFFFFFFFF
                h4 = (self.h[4] + h4) & 0xFFFFFFFF
            # Remember the current hash
            self._cached_hash = [h0, h1, h2, h3, h4]
        return self._cached_hash

# Example usage:
if __name__ == '__main__':
    _sha1 = SHA1()
    from sys import argv
    from hashlib import sha1
    try:
        if len(argv) < 2: raise IndexError("No strings passed as arguments")
        for string in argv[1:]:
            _sha1.load(string)
            print(f"(+) Data:\"{string}\"|Hash:{_sha1}|Valid:{sha1(string.encode()).hexdigest()==str(_sha1)}")
    except IndexError:
        string = input("(*) Enter Plain Text >. ")
        _sha1.load(string)
        print(f"(+) Data:\"{string}\"|Hash:{_sha1}|Valid:{sha1(string.encode()).hexdigest()==str(_sha1)}")
