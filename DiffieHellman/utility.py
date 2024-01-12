from math import sqrt

# -----------------------
# required functions
# -----------------------

# utilizes the 6k +/- 1 theory
def is_prime(value:int) -> bool:
    # n is the number to be check whether it is prime or not

    # this flag maintains status whether the n is prime or not

    if (value > 1):
        for i in range(2,int(sqrt(value) + 1)):
            if (value % i == 0): return True
    else: return False


def is_num(value:str) -> bool:
    try: return int(value) == int(value)
    except ValueError: raise ValueError('Input must be a number')
    

# this is not needed in python 
# but was requested in assignment
def square_n_multiply(base:int, power:int, mod='') -> int: 
    # Handling negative powers
    if power < 0: 
        try: 
            base = pow(base, -1, mod)
            power = abs(power)
        except TypeError: 
            raise ValueError("Power must be a non-negative integer.")
    
    result = 1
    while power > 0:
        # only multiple the results by the base
        # if least significat bit of the power is 1
        if power % 2 == 1: result *= base
        # square the base
        base *= base
        # shifting to the next bit
        # by dividing the power by 2
        power //= 2
    return result

# this is not needed in python 
# but was requested in assignment
def gcdExtended(a, b): 
    # Base Case 
    if a == 0 : 
        return b,0,1
             
    gcd,x1,y1 = gcdExtended(b%a, a) 
     
    # Update x and y using results of recursive 
    # call 
    x = y1 - (b//a) * x1 
    y = x1 
     
    return gcd,x,y 

# ----------------------------
# simplification functions
# ----------------------------


def encode(text:str) -> list:
    return [ord(x) for x in list(text)]

def decode(code:list) -> str:
    return ''.join([chr(_) for _ in code])


if __name__ == '__main__':
    print("(i) testing encoding and decoding")
    print('(+) encoded \'hi\' is ' + str(encode('hi')))
    print('(+) decoded [104, 105] is \"' + str(decode(encode('hi'))) + '\"')
