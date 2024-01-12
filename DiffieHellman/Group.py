import DiffieHellman.utility

class Albelian(object):
    # constructor
    def __init__(self, modulus:int, elements=None, star=True):
        
        if DiffieHellman.utility.is_prime(modulus): raise ValueError("Modulus should be a prime number in Albelain groups")
        #if modulus < 10 : raise ValueError("Modulus too small to form a group")

        # does the modulus operation before loading given elements
        if elements == None: self.elements = set(range(int(star),modulus))
        else: self.elements = set([x % modulus for x in elements])
        
        # stored for later usage
        self.modulus = modulus

    # Private Methods
    # intended for internal use only

    def __eorder(self, x:int) -> int:
        order = 1
        # it should generate a set from an element
        while (
        # by applying it to itself with multiplication oprand
            pow(x, order, self.modulus) != 1 and 
            # no infinite loops plz
            order <= self.modulus 
        # then count the generated elements 
        ): order +=1
        return order

    def __is_generator__(self, x:int) -> bool:
        return self.__eorder(x) == self.order

    @property
    def order(self) -> int: return len(self.elements)
    
    def generators(self) -> list:
        out = []
        for e in self.elements:
            if self.__is_generator__(e) : out.append(e)
        return out

# testing our class
if __name__ == '__main__':
    g = Albelian(11,elements=[1,2,3,4,5,6,7,8,9,10])
    print(g.generators())

