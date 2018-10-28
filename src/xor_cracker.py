from codecs import decode
from base64 import b64encode, b64decode
from functools import partial, reduce
import operator
import enchant
import xor_tools
import character_frequency as cf


def score_cracked_message_with_character_frequency(msg, key):
    freq = cf.english_character_frequency()
    freq[' '] = 0.1
    return (sum([freq.get(c, 0) for c in msg.lower()]), msg, key)

def score_cracked_message_with_distribution_similarity(msg, key):
    x_scale = cf.x_scale()
    try:
        edf_1 = partial(cf.edf, freqs = cf.character_frequency(msg, x_scale), x_scale = x_scale)
    except AssertionError:
        return (-1000000, msg, key)

    edf_2 = partial(cf.edf, freqs = cf.english_character_frequency(), x_scale = x_scale)

    ks = cf.kolmogorov_smirnow(edf_1, edf_2, x_scale)
    return (-1 * ks, msg, key)

def score_cracked_message_with_character_percentage(msg, key):
    if (len(msg) > 0):
        score = cf.percentage_of_characters(msg)
        return (score, msg, key)

    return (-1, msg, key)

def score_cracked_message_with_dictionary(msg, key, dictionary = enchant.Dict("en_US")):
    if (len(msg) > 0 and cf.are_most_chars_letters(msg)):
        try:
            score = sum([dictionary.check(word) for word in msg.split(' ')])
        except:
            score = -1
    else:
        score = -1

    return (score, msg, key)

def average_hamming_distance(msg, block_size, n):
    return sum([cf.normalized_hamming_distance(msg[block_size * x : block_size * (x + 1)],
                                        msg[block_size * (x + 1): block_size * (x + 2)])
     for x in range(0, n*2, 2)]) / n

def single_byte_xor_cipher_cracker(xs, scorer = score_cracked_message_with_character_percentage):
    msgs = [scorer(decode(xor_tools.single_byte_xor(xs, key), 'utf-8', errors = 'ignore'), key)
            for key in range(0, 256)]

    return max(msgs, key = operator.itemgetter(0))

def divide_to_blocks(msg, columns):
    return [msg[x:x+columns] for x in range(0, len(msg), columns)]

def transpose(block):
    return [reduce(lambda acc, b: acc + b[x:x+1], block)
            for x
            in range(0, len(block[0]))]

def deduce_most_probable_keysizes(msg):
    keysize_scores = [(keysize, average_hamming_distance(msg, keysize, 8))
                      for keysize in range(2, 41)]

    return [keysize for keysize, hd in sorted(keysize_scores, key = operator.itemgetter(1))[0:3]]

def break_repeating_key_xor(encrypted_msg):
    tblocks = [transpose(divide_to_blocks(encrypted_msg, keysize))
               for keysize
               in deduce_most_probable_keysizes(encrypted_msg)]

    keys = [bytes([single_byte_xor_cipher_cracker(x, scorer = score_cracked_message_with_character_frequency)[2]
                   for x in block])
            for block in tblocks]

    cracked_msgs = [xor_tools.repeating_xor(encrypted_msg, key) for key in keys]

    return max([score_cracked_message_with_dictionary(msg.decode(), key.decode())
                for msg, key in zip(cracked_msgs, keys)],
               key = operator.itemgetter(0))

def read_base64_file_to_bytearray(filepath):
    with open(filepath, 'r') as f:
        content = f.read().strip("\n")
        encrypted_msg = b64decode(content)

    return encrypted_msg

def detect_single_character_xor(filepath="data/4.txt", dictionary = enchant.Dict("en_US")):
    msgs = []
    with open(filepath, 'r', encoding = 'utf-8') as f:
        encr_msg = f.readline()
        while encr_msg:
           msg = single_byte_xor_cipher_cracker(decode(bytes(encr_msg.strip('\n'), 'utf-8'), 'hex'),
                                                partial(score_cracked_message_with_dictionary , dictionary = dictionary))

           msgs.append({
               'encrypted_msg': encr_msg,
               'msg': msg
           })

           encr_msg = f.readline()

    return max(msgs, key = lambda x: x['msg'][0])

if __name__ == '__main__':
    pass
