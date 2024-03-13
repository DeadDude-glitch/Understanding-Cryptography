from bitarray import bitarray
from DES.Fbox import table
from DES.Ebox import Ebox
from DES.Sbox import Sbox


def straight_premutation(data:bitarray) -> bitarray: 
    result = [data[index-1] for index in table.SP]
    return bitarray(result)


def Fbox(data:bitarray, key:bitarray) -> bitarray:     
    data = Ebox(data)
    data = Sbox(data ^ key)
    data = straight_premutation(data)
    return data

