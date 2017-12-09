import re
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
    'ㄱ' : 'g',
    'ㄲ' : 'kk',
    'ㅋ' : 'k',
    'ㄷ' : 'd',
    'ㄸ' : 'tt',
    'ㅌ' : 't',
    'ㅂ' : 'b',
    'ㅃ' : 'pp',
    'ㅍ' : 'p',
    # 파찰음 affricates
    'ㅈ' : 'j',
    'ㅉ' : 'jj',
    'ㅊ' : 'ch',
    # 마찰음 fricatives
    'ㅅ' : 's',
    'ㅆ' : 'ss',
    'ㅎ' : 'h',
    # 비음 nasals
    'ㄴ' : 'n',
    'ㅁ' : 'm',
    # 유음 liquids
    'ㄹ' : 'r',
    # Null sound
    'ㅇ' : '',
}

'''
종성 Jongseong (Syllable Coda)

"The 7 Jongseongs (7종성)"
Only the seven consonants below may appear in coda position
'''

coda = {
    # 파열음 stops/plosives
    'ㄱ' : 'k',
    'ㄷ' : 't',
    'ㅂ' : 'p',
    # 비음 nasals
    'ㄴ' : 'n',
    'ㅇ' : 'ng',
    'ㅁ' : 'm',
    # 유음 liquids
    'ㄹ' : 'l',
    
    None: '',
    'ㅆ': 't',
    'ㅅ': 't',
    'ㄶ': 'n',
    'ㅎ': None,
}

unicode_initial = [ 'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
unicode_medial = [ 'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
unicode_final = [ None,  'ㄱ',  'ㄲ',  'ㄳ',  'ㄴ',  'ㄵ',  'ㄶ',  'ㄷ',  'ㄹ',  'ㄺ',  'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ','ㅀ', 'ㅁ', 'ㅂ', 'ㅄ',  'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

class Syllable(object):
    def __init__(self, char):
        _separated = self.separate_syllable(char)
        self.char = char
        self.initial = unicode_initial[_separated[0]]
        self.medial = unicode_medial[_separated[1]]
        self.final = unicode_final[_separated[2]]
    
    def separate_syllable(self, char):
        initial = (ord(char)-44032) // 588
        medial = ((ord(char)-44032) - 588 * initial) // 28
        final = (((ord(char)-44032) - 588 * initial) - 28 * medial)

        return(initial, medial, final)

class Romanizer(object):
    def __init__(self, text):
        self.text = text

    def romanize(self):
        hangul = r"[가-힣ㄱ-ㅣ]"
        _romanized = ""
        for char in self.text:
            if (re.match(hangul, char)):
                s = Syllable(char)
                try:
                    _romanized += onset[s.initial] + vowel[s.medial] + coda[s.final]
                except TypeError:
                    _romanized += "[에러:" + s.char + "]"
            else:
                _romanized += char

        return _romanized