from codecs import encode, decode
from functools import partial
import crypto_utils
import xor_tools
import xor_cracker
import character_frequency as cf


def challenge_1_convert_hex_to_base64():
    result = crypto_utils.hex_to_base64(b'49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d')
    answer = b'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'
    return (result, answer, result == answer)

def challenge_2_fixed_xor():
    result = xor_tools.fixed_xor(decode(b'1c0111001f010100061a024b53535009181c', 'hex'),
                                 decode(b'686974207468652062756c6c277320657965', 'hex'))
    answer = b'746865206b696420646f6e277420706c6179'
    return (result, answer, result == answer)

def challenge_3_single_byte_xor_cipher():
    return xor_cracker.single_byte_xor_cipher_cracker(decode(
        b'1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736',
        'hex'))

def challenge_4_detect_single_character_xor():
    return xor_cracker.detect_single_character_xor("data/4.txt")

def challenge_5_repeating_xor():
    msg = b"""Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""
    result = encode(xor_tools.repeating_xor(msg, b'ICE'), 'hex')
    answer = b'0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'
    return (result, answer, result == answer)

def challenge_6_break_repeating_key_xor():
    return xor_cracker.crack_repeating_key_xor(crypto_utils.read_base64_file_to_bytearray('data/6.txt'))


if __name__ == '__main__':
    print("Challenge 1 -- Convert hex to base64:\n", challenge_1_convert_hex_to_base64(), "\n")
    print("Challenge 2 -- Fixed XOR:\n", challenge_2_fixed_xor(), "\n")
    print("Challenge 3 -- Single-byte XOR cipher:\n", challenge_3_single_byte_xor_cipher(), "\n")
    print("Challenge 4 -- Detect single-character XOR:\n", challenge_4_detect_single_character_xor(), "\n")
    print("Challenge 5 -- Implement repeating-key XOR:\n", challenge_5_repeating_xor(), "\n")
    print("Challenge 6 -- Break repeating-key XOR:\n", challenge_6_break_repeating_key_xor(), "\n")
