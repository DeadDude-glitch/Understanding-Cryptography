#!/bin/python3
if __name__  != "__main__":  print("(-) this is a driver code. must run as __main__")

import DES
from bitarray import bitarray

def hex_to_bits(value:str) -> bitarray:
    bvalue = bin(int(value, 16))[2:]
    return bitarray(bvalue)

def bits_to_hex(value:bitarray) -> str: 
    return value.tobytes().hex().upper()

def left_pad(value:bitarray, count:int, insertedvalue=0) -> bitarray:
    while len(value) < count: value.insert(0,insertedvalue)
    return value

plaintext = hex_to_bits('0123456789ABCDEF')
plaintext = left_pad(plaintext, 64)
print("plain text:", bits_to_hex(plaintext))
secret_msg = '266200199BBCDFF1'
password = left_pad(
    hex_to_bits('266200199BBCDFF1'),
    64
)
keys = DES.generate_key(password)
cipher = DES.encrypt(plaintext, keys)
print("cipher:  ", bits_to_hex(cipher))
print("expected: 4E0E6864B5E1CA52")
