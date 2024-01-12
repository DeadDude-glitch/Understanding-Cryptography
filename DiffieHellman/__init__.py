import DiffieHellman.Group
import DiffieHellman.utility
from random import randrange


class Key(object):

    def __init__(self, prime:int, alpha=None, pubkey=None):
        # init the crypto-system
        if prime < 4 : raise ValueError("Prime is too small to form a proper group")
        self.group = Group.Albelian(prime)
        
        if alpha == None : # find a primitive if none exist 
            alpha = self.group.generators()[1] 
        self.alpha = alpha
        
        # generate keys
        self.private = self.gen_pri_key()
        self.public = self.gen_pub_key()
        self._shared = None

        if pubkey == None: self._shared = None
        else: self._shared = self.gen_shared_key(pubkey)
    
    def shared(self, pubkey=None) -> int: 
        if self._shared != None: return self._shared
        elif pubkey != None : return self.gen_shared_key(pubkey)
        return None
        # auto setting shared key
        #if self.gen_shared_key(pubkey): return self._shared
        #return None

    # reset the shared key to reuse the cipher
    def reset(self): self._shared = None

    @property
    def prime(self): return self.group.modulus

    def gen_shared_key(self, pbkey) -> int:
        if self._shared != None : return self.shared()
        try: 
            self._shared = pow(pbkey, self.private, self.prime)
            return self._shared
        except TypeError: 
            print("(-) No public keys were exchanged")
            return None
    
    def gen_pub_key(self) -> int:
        return pow(self.alpha,self.private,self.prime)
    
    def gen_pri_key(self): 
        # random private key in [2,p-2]
        return randrange(2, self.prime-2)


def exchange(k1:Key, k2:Key) -> True:
    # Make sure both are in the same group
    if int(k1.prime) != int(k2.prime) : 
        print('(-) Prime values are not equal ')
        return False
    
    if int(k1.alpha) != int(k2.alpha) :
        print('(-) Primitives values are not equal ')
        return False
    
    try:
        # exchanging public keys
        k1.shared(k2.public)
        k2.shared(k1.public)
        return True
    except TypeError: return False

if __name__ == '__main__':
    print("(+) No Syntax Errors")

