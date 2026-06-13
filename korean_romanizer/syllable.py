"""
Hangul syllable decomposition and reconstruction.

A Syllable object decomposes a single Hangul character into its
structural components: initial consonant (choseong), medial vowel (jungseong),
and final consonant (jongseong/coda).
"""
from korean_romanizer.tables import (
    NULL_CONSONANT,
    unicode_compatible_consonants,
    unicode_compatible_finals,
    unicode_final,
    unicode_initial,
    unicode_initial_offset,
    unicode_medial,
    unicode_medial_offset,
    unicode_offset,
)

# Named constant for the start of Unicode initial jamo block
_UNICODE_INITIAL_START = 4352


class Syllable(object):
    def __init__(self, char):
        self.char = char
        _is_hangul, _separated = self._decompose(char)
        if _is_hangul:
            self.initial = unicode_initial[_separated[0]]
            self.medial = unicode_medial[_separated[1]]
            self.final = unicode_final[_separated[2]]
        else:
            self.initial = _separated[0]
            self.medial = None
            self.final = None

    @staticmethod
    def _decompose(char):
        """Decompose a character into its Unicode component indices."""
        if _is_composed_syllable_block(char):
            initial = (ord(char) - unicode_offset) // unicode_initial_offset
            medial = ((ord(char) - unicode_offset) - unicode_initial_offset * initial) // unicode_medial_offset
            final = ((ord(char) - unicode_offset) - unicode_initial_offset * initial) - unicode_medial_offset * medial
        else:
            initial = ord(char)
            medial = None
            final = None
        return _is_composed_syllable_block(char), [initial, medial, final]

    def _compose(self, initial, medial, final):
        """Compose a Hangul character from its components. Pure function (no mutation)."""
        if _is_composed_syllable_block(self.char):
            initial_idx = ord(initial) - _UNICODE_INITIAL_START
            medial_idx = unicode_medial.index(medial)
            if final is None:
                final_idx = 0
            else:
                final_idx = unicode_final.index(final)
            return chr((((initial_idx * unicode_initial_offset) + (medial_idx * unicode_medial_offset)) + final_idx) + unicode_offset)
        else:
            return self.char

    def sync_char(self):
        """Reconstruct self.char from current initial/medial/final after mutation."""
        self.char = self._compose(self.initial, self.medial, self.final)
        return self.char

    def final_to_initial(self, char):
        """Convert a final (jongseong) jamo to its initial (choseong) equivalent."""
        idx = unicode_compatible_finals.index(char)
        return unicode_initial[idx]

    def __repr__(self):
        return self._compose(self.initial, self.medial, self.final)

    def __str__(self):
        return self._compose(self.initial, self.medial, self.final)


def _is_composed_syllable_block(char):
    """Check if a character is a composed Hangul syllable block (U+AC00–U+D7A3)."""
    return 0xAC00 <= ord(char) <= 0xD7A3


def is_hangul_char(char):
    """Check if a character is any romanizable Hangul (syllable block or jamo)."""
    return '가' <= char <= '힣' or 'ㄱ' <= char <= 'ㅣ'
