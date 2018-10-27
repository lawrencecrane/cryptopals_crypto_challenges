from base64 import b64encode
from codecs import encode, decode

def hex_to_base64(x):
    return b64encode(decode(x, 'hex'))

def fixed_xor(xs, ys):
    assert len(xs) == len(ys)
    return encode(bytes([x ^ y for x, y in zip(decode(xs, 'hex'), decode(ys, 'hex'))]), 'hex')

if __name__ == '__main__':
    print(fixed_xor(b'1c0111001f010100061a024b53535009181c',
                    b'686974207468652062756c6c277320657965'))

    print(fixed_xor(b'1c0111001f010100061a024b53535009181c',
                    b'1c0111001f010100061a024b53535009181c'))
