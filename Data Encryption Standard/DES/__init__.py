#from DES import Key
from DES import Key
from DES import Fbox
from DES import table
from bitarray import bitarray # DOCS: https://pypi.org/project/bitarray/

# this code a customized implementation of the DES encryption
# was written as cryptography assignment in Cairo University

# useless functions that do nothing security-wise
# one of the creators said its about the circuit development
# the book author of "Understanding Cryptography"
# Christof Paar said coding them is useless and a time waste

def initial_premutation(data:bitarray) -> bitarray: 
    # replace values of result of index i with the the IP[i]th of data
    result = [data[index-1] for index in table.IP]
    return bitarray(result)

def final_premutation(data:str) -> str:
    result = [data[index-1] for index in table.FP]
    return bitarray(result)


def encryption_round(DataBlock:bitarray, key:bitarray):
    #result = ( DataBlock[32:] ^ Fbox.Fbox(DataBlock[:32], key)) + bitarray(DataBlock[:32])
    result = DataBlock[32:] +  (DataBlock[:32] ^ Fbox.Fbox(DataBlock[32:], key))
    return result

def encrypt(data:bitarray, secret:list):
    # initial premutation
    data = initial_premutation(data)
    # encryption
    for key in secret:
        # split data into Lside and Rside
        data = encryption_round(data, key)
    data = data[32:] + data[:32]
    data = final_premutation(data)
    return data


def generate_key(secret:bitarray) -> list: 
    keys = []
    secret = Key.initial_premutation(secret)
    for i in range(16):
        secret = Key.transformation(secret, i)
        keys.append(Key.round_premutation(secret))
    return keys

