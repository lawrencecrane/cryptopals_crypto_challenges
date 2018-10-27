from codecs import encode, decode
from itertools import cycle


def fixed_xor(xs, ys):
    assert len(xs) == len(ys)
    return encode(bytes([x ^ y for x, y in zip(decode(xs, 'hex'), decode(ys, 'hex'))]), 'hex')

def single_byte_xor(xs, y):
    assert isinstance(y, int)
    assert y >= 0 and y <= 256

    return bytes([x ^ y for x, y in zip(decode(xs, 'hex'), cycle(bytes([y])))])

def repeating_xor(xs, key):
    return encode(bytes([x ^ y for x, y in zip(xs, cycle(key))]), 'hex')
