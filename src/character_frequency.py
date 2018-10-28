from string import ascii_lowercase as letters
from functools import reduce


def percentage_of_characters(xs):
    assert len(xs) > 0
    return len([c for c in xs if letters.find(c) >= 0]) / len(xs)

def are_most_chars_letters(xs):
    return percentage_of_characters(xs) > 0.5

def hamming_distance(xs, ys):
    assert len(xs) == len(ys)
    return sum(bin(a^b).count("1") for a, b in zip(xs, ys))

def normalized_hamming_distance(a, b):
    assert len(a) == len(b)
    return hamming_distance(a, b) / len(a)

def x_scale():
    return 'etaoinshrdlcumwfgypbvkjxqz'[::-1]

def english_character_frequency():
    return {
        'a': 0.08167,
        'b': 0.01492,
        'c': 0.02782,
        'd': 0.04253,
        'e': 0.12702,
        'f': 0.02228,
        'g': 0.02015,
        'h': 0.06094,
        'i': 0.06966,
        'j': 0.00153,
        'k': 0.00772,
        'l': 0.04025,
        'm': 0.02406,
        'n': 0.06749,
        'o': 0.07507,
        'p': 0.01929,
        'q': 0.00095,
        'r': 0.05987,
        's': 0.06327,
        't': 0.09056,
        'u': 0.02758,
        'v': 0.00978,
        'w': 0.02360,
        'x': 0.00150,
        'y': 0.01974,
        'z': 0.00074
    }

def character_frequency(msg, characters):
    msg_filtered = [x for x in msg.lower() if characters.find(x) >= 0]
    assert len(msg_filtered) > 0

    return {c: msg_filtered.count(c) / len(msg_filtered) for c in characters}

def edf(x, freqs, x_scale):
    return sum([freqs[key] for key in x_scale[0:x_scale.find(x) + 1]])

def kolmogorov_smirnow(edf_1, edf_2, xs):
        return max([abs(edf_1(x) - edf_2(x)) for x in xs])
