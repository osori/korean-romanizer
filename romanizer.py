import re
'''
### Transcribing vowels ###
'''

NULL_CONSONANT = 'ㅇ'

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
}

unicode_initial = [ 'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
unicode_initial = [ chr(initial_code) for initial_code in range(4352, 4371)]
unicode_medial = [ 'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']

#unicode_final = [ None,  'ㄱ',  'ㄲ',  'ㄳ',  'ㄴ',  'ㄵ',  'ㄶ',  'ㄷ',  'ㄹ',  'ㄺ',  'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ','ㅀ', 'ㅁ', 'ㅂ', 'ㅄ',  'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
unicode_final = [ chr(final_code) for final_code in range(0x11a8, 0x11c2)]
unicode_final.insert(0, None)

class Syllable(object):
    def __init__(self, char):
        _separated = self.separate_syllable(char)
        self.char = char
        if (self.is_hangul()):
            self.initial = unicode_initial[_separated[0]]
            self.medial = unicode_medial[_separated[1]]
            self.final = unicode_final[_separated[2]]
        else:
            self.initial = self.char
            self.medial = None
            self.final = None
    
    def separate_syllable(self, char):
        initial = (ord(char)-44032) // 588
        medial = ((ord(char)-44032) - 588 * initial) // 28
        final = (((ord(char)-44032) - 588 * initial) - 28 * medial)
        print("Separate", initial,medial,final)
        return(initial, medial, final)
    
    def construct_syllable(self, initial, medial, final):
        initial = ord(initial) - 4352
        medial = unicode_medial.index(medial)
        if final is None:
            final = 0
        else:
            final = unicode_final.index(final)
        print("Construct", initial,medial,final)
        constructed = chr((((initial * 588) + (medial * 28)) + final) + 44032)
        return constructed
    
    def is_hangul(self):
        return True if 0xAC00 <= ord(self.char) <= 0xD7A3 else False
    
    def __repr__(self):
        return self.construct_syllable(self.initial, self.medial, self.final)
    
    def __str__(self):
        return self.construct_syllable(self.initial, self.medial, self.final)

class Pronouncer(object):
    def __init__(self, text):
        self._syllables = [Syllable(char) for char in text]
        self.pronounced = ''.join([ str(c) for c in self.final_substitute()])
    
    
    def final_substitute(self):
        for idx, syllable in enumerate(self._syllables):
            try:
                next_syllable = self._syllables[idx+1]
                final_is_before_C = syllable.final and next_syllable != NULL_CONSONANT
            except IndexError:
                next_syllable = None
                
            # 1. 받침 ‘ㄲ, ㅋ’, ‘ㅅ, ㅆ, ㅈ, ㅊ, ㅌ’, ‘ㅍ’은 어말 또는 
            # 자음 앞에서 각각 대표음 [ㄱ, ㄷ, ㅂ]으로 발음한다.
            # <-> 단, 국어의 로마자 표기법 규정에 의해 된소리되기는 표기에 반영하지 않으므로 제외.
            if(syllable.final or final_is_before_C): 
                if(syllable.final in ['ᆩ', 'ᆿ', 'ᆪ']):
                    syllable.final = 'ᆨ'
                elif(syllable.final in ['ᆺ', 'ᆻ', 'ᆽ', 'ᆾ', 'ᇀ']):
                    syllable.final = 'ᆮ'
                elif(syllable.final in ['ㅍ', 'ᆹ']):
                    syllable.final = 'ᆸ'
                elif(syllable.final in ['ᆬ']):
                    syllable.final = 'ᆫ'
                elif(syllable.final in ['ᆲ', 'ᆳ', 'ᆴ']):
                    syllable.final = 'ᆯ'
                    
        return self._syllables
                

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
    
    
Pronouncer("앏").pronounced