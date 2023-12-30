import struct

class SHA1(object):

    # Static Variables
    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    k = [0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xCA62C1D6]

    # Constructor
    def __init__(self):
        self._message = b""
        self._cached_hash = None

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
        if len(h) != 3 : raise IndexError("h must be an array of 4 values")
        b, c ,d = h
        if   loop_number % 80 < 20: return (h[0] & h[1]) | ((~h[0]) & h[2])
        elif loop_number % 80 < 40: return  h[0] ^ h[1] ^ h[2]
        elif loop_number % 80 < 60: return (h[0] & h[1]) | (h[0] & h[2]) | (h[1] & h[2])
        else: return h[0] ^ h[1] ^ h[2]


    @staticmethod
    def round(loop_number:int, h:list, word:list) -> list:
        temp = ((h[0] << 5 | h[0] >> 27) & 0xFFFFFFFF) + self.f(loop_number,h[1:3]) + e + self.k[int(loop_number/20)%4] + words[loop_number] & 0xFFFFFFFF
        h[4], h[3], h[2], h[1], h[0] = h[3], h[2], (h[1] << 30 | h[1] >> 2) & 0xFFFFFFFF, h[0], temp
        return h

    def load(self, text:str) -> bool:
        self._message = text.encode()
        self._cached_hash = None
        return True

    def hash(self, rounds:int=80, format='bytes'):
        if self._cached_hash != None :
            h0, h1, h2, h3, h4 = self._cached_hash
        else:
            # Initialize hash values
            h0, h1, h2, h3, h4 = self.h

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
                a, b, c, d, e = h0, h1, h2, h3, h4
                # main round
                for j in range(rounds):
                    temp = ((a << 5 | a >> 27) & 0xFFFFFFFF) + self.f(j,[b,c,d]) + e + self.k[int(j/20)%4] + words[j] & 0xFFFFFFFF
                    e, d, c, b, a = d, c, (b << 30 | b >> 2) & 0xFFFFFFFF, a, temp
                h0 = (h0 + a) & 0xFFFFFFFF
                h1 = (h1 + b) & 0xFFFFFFFF
                h2 = (h2 + c) & 0xFFFFFFFF
                h3 = (h3 + d) & 0xFFFFFFFF
                h4 = (h4 + e) & 0xFFFFFFFF
            # Remember the current hash
            self._cached_hash = [h0, h1, h2, h3, h4]

        # Produce the final hash
        if format == 'hex':
            return '{:08x}{:08x}{:08x}{:08x}{:08x}'.format(h0, h1, h2, h3, h4)
        if format == "bytes":
            return struct.pack('>5L', h0, h1, h2, h3, h4)
        else: raise ValueError(f"format {format} is not supported")

# Example usage:
if __name__ == '__main__':
    _sha1 = SHA1()
    from sys import argv
    from hashlib import sha1
    try:
        if len(argv) < 2: raise IndexError("No strings passed as arguments")
        for string in argv[1:]:
            _sha1.load(string)
            print(f"(+) Data:\"{string}\"|Hash:{_sha1.hash(format='hex')}|Valid:{sha1(string.encode()).hexdigest()==_sha1.hash(format='hex')}")
    except IndexError:
        string = input("(*) Enter Plain Text >. ")
        _sha1.load(string)
        print(f"(+) Data:\"{string}\"|Hash:{_sha1.hash(format='hex')}|Valid:{sha1(string.encode()).hexdigest()==_sha1.hash(format='hex')}")
