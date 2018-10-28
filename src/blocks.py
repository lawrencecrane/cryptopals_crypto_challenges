from functools import reduce
import character_frequency as cf


def average_hamming_distance(msg, block_size, n):
    return sum([cf.normalized_hamming_distance(msg[block_size * x : block_size * (x + 1)],
                                        msg[block_size * (x + 1): block_size * (x + 2)])
     for x in range(0, n*2, 2)]) / n

def divide_to_blocks(msg, columns):
    return [msg[x:x+columns] for x in range(0, len(msg), columns)]

def transpose(block):
    return [reduce(lambda acc, b: acc + b[x:x+1], block)
            for x
            in range(0, len(block[0]))]
