from bitarray import bitarray
from bitarray.util import ba2int, int2ba
from DES.Sbox import table

def Sbox(data:bitarray) -> bitarray:
    result = bitarray()
    for i in range(8):
        row = data[i * 6]*2 + data[i * 6 + 5]  # Calculate row index
        col = ba2int(data[i * 6 + 1 : i * 6 + 5])  # Calculate column index
        result.extend(int2ba(table.S[i][row][col],length=4))
    return result
