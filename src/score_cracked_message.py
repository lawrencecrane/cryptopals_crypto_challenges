from functools import partial
import enchant
import character_frequency as cf

def character_frequency(msg, key):
    freq = cf.english_character_frequency()
    freq[' '] = 0.1
    return (sum([freq.get(c, 0) for c in msg.lower()]), msg, key)

def distribution_similarity(msg, key):
    x_scale = cf.x_scale()
    try:
        edf_1 = partial(cf.edf, freqs = cf.character_frequency(msg, x_scale), x_scale = x_scale)
    except AssertionError:
        return (-1000000, msg, key)

    edf_2 = partial(cf.edf, freqs = cf.english_character_frequency(), x_scale = x_scale)

    ks = cf.kolmogorov_smirnow(edf_1, edf_2, x_scale)
    return (-1 * ks, msg, key)

def character_percentage(msg, key):
    if (len(msg) > 0):
        score = cf.percentage_of_characters(msg)
        return (score, msg, key)

    return (-1, msg, key)

def dictionary(msg, key, dictionary = enchant.Dict("en_US")):
    if (len(msg) > 0 and cf.are_most_chars_letters(msg)):
        try:
            score = sum([dictionary.check(word) for word in msg.split(' ')])
        except:
            score = -1
    else:
        score = -1

    return (score, msg, key)
