from hypothesis import given, assume, strategies as st
from codecs import encode
import crypto


def test_hex_to_base64():
    assert crypto.hex_to_base64(b'49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d') == b'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

def test_fixed_xor():
    assert crypto.fixed_xor(b'1c0111001f010100061a024b53535009181c',
                            b'686974207468652062756c6c277320657965') == b'746865206b696420646f6e277420706c6179'

@given(st.text())
def test_fixed_xor_idempotency(x):
    a = encode(bytearray(x, 'utf8'), 'hex')
    assert crypto.fixed_xor(a, a) == b'0' * len(a)
