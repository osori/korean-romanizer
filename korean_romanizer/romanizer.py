from korean_romanizer.syllable import (
    Syllable,
    unicode_compatible_consonants,
    unicode_initial,
)
from korean_romanizer.pronouncer import Pronouncer
from korean_romanizer.tables import coda, compat_onset, onset, vowel

INITIAL_RIEUL = 'ᄅ'
FINAL_RIEUL = 'ᆯ'


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


def _romanize_initial(syllable, previous_syllable):
    if (
        syllable.initial == INITIAL_RIEUL
        and previous_syllable
        and previous_syllable.final == FINAL_RIEUL
    ):
        return 'l'

    return onset[syllable.initial]


def _romanize_syllable(char, previous_syllable=None):
    syllable = Syllable(char)

    if not syllable.medial and not syllable.final:
        return _romanize_non_syllable(char), None

    romanized = _romanize_initial(syllable, previous_syllable)
    romanized += vowel[syllable.medial] + coda[syllable.final]
    return romanized, syllable


def romanize(text: str) -> str:
    """Romanize Korean text using this package's rules."""
    pronounced = Pronouncer(text).pronounced
    romanized = []
    previous_syllable = None
    for char in pronounced:
        if _is_romanizable_hangul(char):
            romanized_char, previous_syllable = _romanize_syllable(
                char, previous_syllable)
            romanized.append(romanized_char)
        else:
            romanized.append(char)
            previous_syllable = None

    return ''.join(romanized)


class Romanizer(object):
    """Compatibility wrapper for romanizing Korean text."""

    def __init__(self, text):
        self.text = text

    def romanize(self):
        """Romanize the stored text using the functional API."""
        return romanize(self.text)
