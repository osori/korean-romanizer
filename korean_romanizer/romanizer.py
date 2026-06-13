"""
Korean Hangul romanizer — converts Korean text to Latin script.

Uses the Revised Romanization of Korean (RR) system as specified by
the National Institute of Korean Language.
"""
from korean_romanizer.syllable import Syllable, is_hangul_char
from korean_romanizer.pronouncer import Pronouncer
from korean_romanizer.tables import (
    CODA_ROMANIZATION,
    COMPAT_ONSET_ROMANIZATION,
    ONSET_ROMANIZATION,
    VOWEL_ROMANIZATION,
)


def _romanize_standalone_jamo(char):
    """Romanize a standalone jamo character (compatibility consonant or vowel)."""
    if char in VOWEL_ROMANIZATION:
        return VOWEL_ROMANIZATION[char]
    elif char in ONSET_ROMANIZATION:
        return ONSET_ROMANIZATION[char]
    elif char in COMPAT_ONSET_ROMANIZATION:
        return COMPAT_ONSET_ROMANIZATION[char]
    else:
        return char


def _romanize_syllable(char):
    """Romanize a single Hangul syllable block."""
    syllable = Syllable(char)

    if not syllable.medial and not syllable.final:
        return _romanize_standalone_jamo(char)

    return ONSET_ROMANIZATION[syllable.initial] + VOWEL_ROMANIZATION[syllable.medial] + CODA_ROMANIZATION[syllable.final]


class Romanizer(object):
    def __init__(self, text):
        self.text = text

    def romanize(self):
        pronounced = Pronouncer(self.text).pronounced
        romanized = []
        for char in pronounced:
            if is_hangul_char(char):
                romanized.append(_romanize_syllable(char))
            else:
                romanized.append(char)

        return ''.join(romanized)
