from base64 import b64encode
from codecs import encode, decode
from itertools import cycle
from functools import reduce
from string import ascii_lowercase as letters
import re
import operator
import enchant

def hex_to_base64(x):
    return b64encode(decode(x, 'hex'))

def fixed_xor(xs, ys):
    assert len(xs) == len(ys)
    return encode(bytes([x ^ y for x, y in zip(decode(xs, 'hex'), decode(ys, 'hex'))]), 'hex')

def single_byte_xor(xs, y):
    assert isinstance(y, int)
    assert y >= 0 and y <= 256

    return bytes([x ^ y for x, y in zip(decode(xs, 'hex'), cycle(bytes([y])))])

def repeating_xor(xs, key):
    return encode(bytes([x ^ y for x, y in zip(xs, cycle(key))]), 'hex')

def most_chars_are_letters(xs):
    letter_freq = len([c for c in xs if letters.find(c) >= 0]) / len(xs)
    return letter_freq > 0.5

def score_cracked_message(msg, dictionary = enchant.Dict("en_US")):
    if (len(msg) > 0 and most_chars_are_letters(msg)):
        try:
            score = sum([dictionary.check(word) for word in msg.split(' ')])
        except:
            score = -1
    else:
        score = -1

    return (score, msg)

def single_byte_xor_cipher_cracker(xs, dictionary = enchant.Dict("en_US")):
    msgs = [score_cracked_message(decode(single_byte_xor(xs, y), 'utf-8', errors = 'ignore'),
                                  dictionary)
            for y in range(0, 256)]

    return max(msgs, key = operator.itemgetter(0))

def detect_single_character_xor(filepath):
    msgs = []
    with open(filepath, 'r', encoding = 'utf-8') as f:
        encr_msg = f.readline()
        while encr_msg:
           msg = single_byte_xor_cipher_cracker(bytes(encr_msg.strip('\n'), 'utf-8'))
           msgs.append({
               'encrypted_msg': encr_msg,
               'msg': msg
           })

           encr_msg = f.readline()

    return max(msgs, key = lambda x: x['msg'][0])

if __name__ == '__main__':
    msg = b"""Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""
    print(repeating_xor(msg, b'ICE'))
    # print(repeating_xor(b"Burning 'em, if you ain't quick and nimble", b'ICE'))
    # print(repeating_xor(b"I go crazy when I hear a cymbal", b'ICE'))
    # print(repeating_xor(b"Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal", b'ICE'))
