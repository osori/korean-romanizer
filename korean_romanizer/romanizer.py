from korean_romanizer.syllable import (
    Syllable,
    unicode_compatible_consonants,
    unicode_initial,
)
from korean_romanizer.pronouncer import Pronouncer

'''
### Transcribing vowels ###
'''

vowel = {
    # 단모음 monophthongs
    'ㅏ' : 'a',
    'ㅓ' : 'eo',
    'ㅗ' : 'o',
    'ㅜ' : 'u',
    'ㅡ' : 'eu',
    'ㅣ' : 'i',
    'ㅐ' : 'ae',
    'ㅔ' : 'e',
    'ㅚ' : 'oe',
    'ㅟ' : 'wi',
    
    # 이중모음 diphthongs
    'ㅑ' : 'ya',
    'ㅕ' : 'yeo',
    'ㅛ' : 'yo',
    'ㅠ' : 'yu',
    'ㅒ' : 'yae',
    'ㅖ' : 'ye',
    'ㅘ' : 'wa',
    'ㅙ' : 'wae',
    'ㅝ' : 'wo',
    'ㅞ' : 'we',
    'ㅢ' : 'ui', # [붙임 1] ‘ㅢ’는 ‘ㅣ’로 소리 나더라도 ‘ui’로 적는다.
}

'''
### Transcribing consonants ###

Consonants are defined in separate dicts, choseong and jongseong,
for some characters are pronounced differently depending on 
its position in the syllable.

e.g. ㄱ, ㄷ, ㅂ, ㄹ are (g, d, b, r) in onset,
                  but (k, t, p, l) in coda.
e.g. ㅇ is a null sound when placed in onset, but becomes [ng] in coda.
'''

# 초성 Choseong (Syllable Onset)
onset = {
    # 파열음 stops/plosives
    'ᄀ' : 'g',
    'ᄁ' : 'kk',
    'ᄏ' : 'k',
    'ᄃ' : 'd',
    'ᄄ' : 'tt',
    'ᄐ' : 't',
    'ᄇ' : 'b',
    'ᄈ' : 'pp',
    'ᄑ' : 'p',
    # 파찰음 affricates
    'ᄌ' : 'j',
    'ᄍ' : 'jj',
    'ᄎ' : 'ch',
    # 마찰음 fricatives
    'ᄉ' : 's',
    'ᄊ' : 'ss',
    'ᄒ' : 'h',
    # 비음 nasals
    'ᄂ' : 'n',
    'ᄆ' : 'm',
    # 유음 liquids
    'ᄅ' : 'r',
    # Null sound
    'ᄋ' : '',
}

'''
종성 Jongseong (Syllable Coda)

"The 7 Jongseongs (7종성)"
Only the seven consonants below may appear in coda position
'''

coda = {
    # 파열음 stops/plosives
    'ᆨ' : 'k',
    'ᆮ' : 't',
    'ᆸ' : 'p',
    # 비음 nasals
    'ᆫ' : 'n',
    'ᆼ' : 'ng',
    'ᆷ' : 'm',
    # 유음 liquids
    'ᆯ' : 'l',
    
    None: '',
}

# Compatibility jamo (e.g. ㄱ, ㄴ) do not appear as part of a full syllable.
# Map them to their onset romanization so single jamo can be transliterated.
compat_onset = {
    comp: onset[unicode_initial[i]]
    for i, comp in enumerate(unicode_compatible_consonants)
}


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
