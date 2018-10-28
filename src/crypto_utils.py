from base64 import b64encode, b64decode
from codecs import decode


def hex_to_base64(x):
    return b64encode(decode(x, 'hex'))

def read_base64_file_to_bytearray(filepath):
    with open(filepath, 'r') as f:
        content = f.read().strip("\n")
        encrypted_msg = b64decode(content)

    return encrypted_msg
