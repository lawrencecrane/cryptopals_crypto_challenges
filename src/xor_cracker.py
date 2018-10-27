from codecs import decode
from string import ascii_lowercase as letters
import operator
import enchant
import xor_tools


def are_most_chars_letters(xs):
    letter_freq = len([c for c in xs if letters.find(c) >= 0]) / len(xs)
    return letter_freq > 0.5

def score_cracked_message(msg, dictionary = enchant.Dict("en_US")):
    if (len(msg) > 0 and are_most_chars_letters(msg)):
        try:
            score = sum([dictionary.check(word) for word in msg.split(' ')])
        except:
            score = -1
    else:
        score = -1

    return (score, msg)

def single_byte_xor_cipher_cracker(xs, dictionary = enchant.Dict("en_US")):
    msgs = [score_cracked_message(decode(xor_tools.single_byte_xor(xs, y), 'utf-8', errors = 'ignore'),
                                  dictionary)
            for y in range(0, 256)]

    return max(msgs, key = operator.itemgetter(0))

def detect_single_character_xor(filepath="data/4.txt", dictionary = enchant.Dict("en_US")):
    msgs = []
    with open(filepath, 'r', encoding = 'utf-8') as f:
        encr_msg = f.readline()
        while encr_msg:
           msg = single_byte_xor_cipher_cracker(bytes(encr_msg.strip('\n'), 'utf-8'),
                                                dictionary)

           msgs.append({
               'encrypted_msg': encr_msg,
               'msg': msg
           })

           encr_msg = f.readline()

    return max(msgs, key = lambda x: x['msg'][0])


if __name__ == '__main__':
    print(detect_single_character_xor())
