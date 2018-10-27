from base64 import b64encode
from codecs import decode


def hex_to_base64(x):
    return b64encode(decode(x, 'hex'))
