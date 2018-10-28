from hypothesis import given, assume, strategies as st
from codecs import encode, decode
from functools import partial
import crypto_utils
import xor_tools
import xor_cracker
import character_frequency as cf

def test_hex_to_base64():
    assert crypto_utils.hex_to_base64(b'49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d') == b'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

def test_fixed_xor():
    assert xor_tools.fixed_xor(decode(b'1c0111001f010100061a024b53535009181c', 'hex'),
                            decode(b'686974207468652062756c6c277320657965', 'hex')) == b'746865206b696420646f6e277420706c6179'

@given(st.text())
def test_fixed_xor_idempotency(x):
    a = bytes(x, 'utf8')
    assert xor_tools.fixed_xor(a, a) == b'0' * len(encode(a, 'hex'))

def test_repeating_xor():
    msg = b"""Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""
    assert encode(xor_tools.repeating_xor(msg, b'ICE'), 'hex') == b'0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'

def test_english_character_frequency():
    assert round(sum([cf.english_character_frequency()[key] for key in cf.english_character_frequency()]), 4) == 1.0

def test_kolmogorov_smirnow():
    edf_1 = partial(cf.edf, freqs = cf.english_character_frequency(), x_scale = cf.x_scale())
    assert round(cf.kolmogorov_smirnow(edf_1, edf_1, cf.x_scale()), 4) == 0.0

    freqs = cf.english_character_frequency()
    freqs['c'] = freqs['c'] + 0.05
    edf_2 = partial(cf.edf, freqs = freqs, x_scale = cf.x_scale())
    assert round(cf.kolmogorov_smirnow(edf_1, edf_2, cf.x_scale()), 4) == 0.05

def test_hamming_distance():
    a = bytes(b'this is a test')
    b = bytes(b'wokka wokka!!!')
    assert cf.hamming_distance(a, b) == 37


if __name__ == '__main__':
    print(xor_cracker.single_byte_xor_cipher_cracker(decode(
        b'1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736',
        'hex')))
    print(xor_cracker.detect_single_character_xor("data/4.txt"))
    print(xor_cracker.break_repeating_key_xor(xor_cracker.read_base64_file_to_bytearray('data/6.txt')))
