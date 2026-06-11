from korean_romanizer.syllable import Syllable
from korean_romanizer.pronouncer import Pronouncer
from korean_romanizer.tables import coda, compat_onset, onset, vowel


def _is_romanizable_hangul(char):
    return '가' <= char <= '힣' or 'ㄱ' <= char <= 'ㅣ'


def _romanize_non_syllable(char):
    if char in vowel:
        return vowel[char]
    elif char in onset:
        return onset[char]
    elif char in compat_onset:
        return compat_onset[char]
    else:
        return char


def _romanize_syllable(char):
    syllable = Syllable(char)

    if not syllable.medial and not syllable.final:
        return _romanize_non_syllable(char)

    return onset[syllable.initial] + vowel[syllable.medial] + coda[syllable.final]


class Romanizer(object):
    def __init__(self, text):
        self.text = text

    def romanize(self):
        pronounced = Pronouncer(self.text).pronounced
        romanized = []
        for char in pronounced:
            if _is_romanizable_hangul(char):
                romanized.append(_romanize_syllable(char))
            else:
                romanized.append(char)

        return ''.join(romanized)
