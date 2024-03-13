from bitarray import bitarray
from DES.Key import table


def round_premutation(data:bitarray) -> bitarray: 
    result = [data[index-1] for index in table.compression_permutation]
    return bitarray(result)


def initial_premutation(data:bitarray) -> bitarray: 
    # replace values of result of index i with the the key_permutation_table [i]th of data
    result = bitarray([data[index-1] for index in table.key_permutation])
    return bitarray(result)


def transformation(password:bitarray, round:int=0) -> bitarray: 
    c = password[:28]
    d = password[28:]
    result = c[table.rotate_order[round]:] + c[:table.rotate_order[round]] + d[table.rotate_order[round]:] + d[:table.rotate_order[round]]
    return result
