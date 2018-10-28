from codecs import decode
from functools import partial, reduce
import operator
import enchant
import xor_tools
import character_frequency as cf
import score_cracked_message as score
import blocks


def deduce_most_probable_keysizes(msg):
    keysize_scores = [(keysize, blocks.average_hamming_distance(msg, keysize, 8))
                      for keysize in range(2, 41)]

    return [keysize for keysize, hd in sorted(keysize_scores, key = operator.itemgetter(1))[0:3]]

def single_byte_xor_cipher_cracker(xs, scorer = score.character_percentage):
    msgs = [scorer(decode(xor_tools.single_byte_xor(xs, key), 'utf-8', errors = 'ignore'), key)
            for key in range(0, 256)]

    return max(msgs, key = operator.itemgetter(0))

def crack_repeating_key_xor(encrypted_msg):
    tblocks = [blocks.transpose(blocks.divide_to_blocks(encrypted_msg, keysize))
               for keysize
               in deduce_most_probable_keysizes(encrypted_msg)]

    keys = [bytes([single_byte_xor_cipher_cracker(x, scorer = score.character_frequency)[2]
                   for x in block])
            for block in tblocks]

    cracked_msgs = [xor_tools.repeating_xor(encrypted_msg, key) for key in keys]

    return max([score.dictionary(msg.decode(), key.decode())
                for msg, key in zip(cracked_msgs, keys)],
               key = operator.itemgetter(0))

def detect_single_character_xor(filepath="data/4.txt", dictionary = enchant.Dict("en_US")):
    msgs = []
    with open(filepath, 'r', encoding = 'utf-8') as f:
        encr_msg = f.readline()
        while encr_msg:
           msg = single_byte_xor_cipher_cracker(decode(bytes(encr_msg.strip('\n'), 'utf-8'), 'hex'),
                                                partial(score.dictionary , dictionary = dictionary))

           msgs.append({
               'encrypted_msg': encr_msg,
               'msg': msg
           })

           encr_msg = f.readline()

    return max(msgs, key = lambda x: x['msg'][0])

if __name__ == '__main__':
    pass
