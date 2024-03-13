from bitarray import bitarray
from DES.Ebox import table
# expand 32 bits to 42 bits using a predefined table
def Ebox(data:bitarray) -> bitarray:
    # replace values of result of index i with the the E[i]th of data
    result = [data[table.E[i]-1] for i in range(48)]
    return bitarray(result)
