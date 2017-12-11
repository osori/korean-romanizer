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

double_consonant_final = {
    'ㄳ' : ('ㄱ', 'ㅅ'),
    'ㄵ' : ('ᆫ', 'ㅈ'), 
    'ᆭ' : ('ᆫ', 'ᇂ'),
    'ㄺ' : ('ㄹ', 'ㄱ'), 
    'ㄻ' : ('ㄹ', 'ㅁ'), 
    'ㄼ' : ('ㄹ', 'ㅂ'), 
    'ㄽ' : ('ㄹ', 'ㅅ'), 
    'ㄾ' : ('ㄹ', 'ㅌ'), 
    'ㄿ' : ('ㄹ', 'ㅍ'),
    'ㅀ' : ('ㄹ', 'ᇂ'), 
    'ㅄ' : ('ㅂ', 'ㅅ'), 
    'ㅆ' : ('ㅅ', 'ㅅ')
}

NULL_CONSONANT = 'ᄋ'

unicode_initial = [ 'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
unicode_initial = [ chr(initial_code) for initial_code in range(4352, 4371)]
unicode_medial = [ 'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']

#unicode_final = [ None,  'ㄱ',  'ㄲ',  'ㄳ',  'ㄴ',  'ㄵ',  'ㄶ',  'ㄷ',  'ㄹ',  'ㄺ',  'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ','ㅀ', 'ㅁ', 'ㅂ', 'ㅄ',  'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
unicode_final = [ chr(final_code) for final_code in range(0x11a8, 0x11c3)]
unicode_final.insert(0, None)

unicode_compatible_consonants = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
unicode_compatible_finals =     ['ᆨ', 'ᆩ', 'ᆫ', 'ᆮ', '_', 'ᆯ', 'ᆷ', 'ᆸ', '_', 'ᆺ', 'ᆻ', 'ᆼ', 'ᆽ', '_', 'ᆾ', 'ᆿ', 'ᇀ', 'ᇁ', 'ᇂ']



class Syllable(object):
    def __init__(self, char):
        self.char = char
        _is_hangul, _separated = self.separate_syllable(char)
        if (_is_hangul):
            self.initial = unicode_initial[_separated[0]]
            self.medial = unicode_medial[_separated[1]]
            self.final = unicode_final[_separated[2]]
        else:
            self.initial = _separated[0]
            self.medial = None
            self.final = None
            
    def separate_syllable(self, char):
        if (self.is_hangul(char)):
            initial = (ord(char)-44032) // 588
            medial = ((ord(char)-44032) - 588 * initial) // 28
            final = (((ord(char)-44032) - 588 * initial) - 28 * medial)
            # print("Separate", initial,medial,final)
        else:
            initial = ord(char)
            medial = None
            final = None
            # print("NOT_HANGUL Separate", initial,medial,final)
            
        return self.is_hangul(char), [initial, medial, final]
    
    def construct_syllable(self, initial, medial, final):
        if self.is_hangul(self.char):
            initial = ord(initial) - 4352
            medial = unicode_medial.index(medial)
            if final is None:
                final = 0
            else:
                final = unicode_final.index(final)
            # print("Construct", initial,medial,final)
            constructed = chr((((initial * 588) + (medial * 28)) + final) + 44032)
        else:
            constructed = self.char
            
        self.char = constructed
        return constructed
    
    def is_hangul(self, char):
        return True if 0xAC00 <= ord(char) <= 0xD7A3 else False
    
    def final_to_initial(self, char):
        idx = unicode_compatible_finals.index(char)
        return unicode_initial[idx]
    
    def __repr__(self):
        self.construct_syllable(self.initial, self.medial, self.final)
        return self.char
    
    def __str__(self):
        self.char = self.construct_syllable(self.initial, self.medial, self.final)
        return self.char

class Pronouncer(object):
    def __init__(self, text):
        self._syllables = [Syllable(char) for char in text]
        self.pronounced = ''.join([ str(c) for c in self.final_substitute()])
    
    
    def final_substitute(self):
        for idx, syllable in enumerate(self._syllables):
            try:
                next_syllable = self._syllables[idx+1]
            except IndexError:
                next_syllable = None
                
            try:    
                final_is_before_C = syllable.final and next_syllable.getattr(initial) not in (None, NULL_CONSONANT)
            except AttributeError:
                final_is_before_C = False
                
            try:    
                final_is_before_V = syllable.final and next_syllable.initial is None
            except AttributeError:
                final_is_before_V = False 
            
            # 1. 받침 ‘ㄲ, ㅋ’, ‘ㅅ, ㅆ, ㅈ, ㅊ, ㅌ’, ‘ㅍ’은 어말 또는 자음 앞에서 각각 대표음 [ㄱ, ㄷ, ㅂ]으로 발음한다.
            # 2. 겹받침 ‘ㄳ’, ‘ㄵ’, ‘ㄼ, ㄽ, ㄾ’, ‘ㅄ’은 어말 또는 자음 앞에서 각각 [ㄱ, ㄴ, ㄹ, ㅂ]으로 발음한다.
            # 3. 겹받침 ‘ㄺ, ㄻ, ㄿ’은 어말 또는 자음 앞에서 각각 [ㄱ, ㅁ, ㅂ]으로 발음한다.
            # <-> 단, 국어의 로마자 표기법 규정에 의해 된소리되기는 표기에 반영하지 않으므로 제외.
            if(syllable.final or final_is_before_C): 
                if(syllable.final in ['ᆩ', 'ᆿ', 'ᆪ', 'ᆰ']):
                    syllable.final = 'ᆨ'
                elif(syllable.final in ['ᆺ', 'ᆻ', 'ᆽ', 'ᆾ', 'ᇀ']):
                    syllable.final = 'ᆮ'
                elif(syllable.final in ['ㅍ', 'ᆹ', 'ᆵ']):
                    syllable.final = 'ᆸ'
                elif(syllable.final in ['ᆬ']):
                    syllable.final = 'ᆫ'
                elif(syllable.final in ['ᆲ', 'ᆳ', 'ᆴ']):
                    syllable.final = 'ᆯ'
                elif(syllable.final in ['ᆱ']):
                    syllable.final = 'ᆷ'
            
            
            # 4. 받침 ‘ㅎ’의 발음은 다음과 같다.
            if syllable.final in ['ᇂ', 'ᆭ', 'ᆶ']:
                
                if next_syllable:
                    # ‘ㅎ(ㄶ, ㅀ)’ 뒤에 ‘ㄱ, ㄷ, ㅈ’이 결합되는 경우에는, 뒤 음절 첫소리와 합쳐서 [ㅋ, ㅌ, ㅊ]으로 발음한다.
                    # ‘ㅎ(ㄶ, ㅀ)’ 뒤에 ‘ㅅ’이 결합되는 경우에는, ‘ㅅ’을 [ㅆ]으로 발음한다.
                    if next_syllable.initial in ['ᄀ', 'ᄃ', 'ᄌ', 'ᄉ']:
                        change_to = {'ᄀ': 'ᄏ','ᄃ': 'ᄐ','ᄌ':'ᄎ', 'ᄉ': 'ᄊ'}
                        syllable.final = None
                        next_syllable.initial = change_to[next_syllable.initial]
                    # 3. ‘ㅎ’ 뒤에 ‘ㄴ’이 결합되는 경우에는, [ㄴ]으로 발음한다.
                    elif next_syllable.initial in ['ᄂ']:
                        # TODO: [붙임] ‘ㄶ, ㅀ’ 뒤에 ‘ㄴ’이 결합되는 경우에는, ‘ㅎ’을 발음하지 않는다.
                        if(syllable.final in ['ᆭ', 'ᆶ']):
                            if syllable.final == 'ᆭ':
                                syllable.final = 'ᆫ'
                            elif syllable.final == 'ᆶ':
                                syllable.final = 'ᆯ' 
                        else:
                            syllable.final = 'ᆫ'
                    #4. ‘ㅎ(ㄶ, ㅀ)’ 뒤에 모음으로 시작된 어미나 접미사가 결합되는 경우에는, 
                    # ‘ㅎ’을 발음하지 않는다.
                    elif next_syllable.initial == NULL_CONSONANT:
                        if(syllable.final in ['ᆭ', 'ᆶ']):
                            if syllable.final == 'ᆭ':
                                syllable.final = 'ᆫ'
                            elif syllable.final == 'ᆶ':
                                syllable.final = 'ᆯ' 
                        else:
                            syllable.final = None
                    else:
                        if (syllable.final == 'ᇂ'):
                            syllable.final = None
                else:
                    if (syllable.final == 'ᇂ'):
                        syllable.final = None
            # 5. 홑받침이나 쌍받침이 모음으로 시작된 조사나 어미, 접미사와 결합되는 경우에는, 
            # 제 음가대로 뒤 음절 첫소리로 옮겨 발음한다. 
            if next_syllable and final_is_before_C:
                if(next_syllable.initial == NULL_CONSONANT):
                    next_syllable.initial = next_syllable.final_to_initial(syllable.final)
                    syllable.final = None
                    
            # 6. 겹받침이 모음으로 시작된 조사나 어미, 접미사와 결합되는 경우에는, 
            # 뒤엣것만을 뒤 음절 첫소리로 옮겨 발음한다.(이 경우, ‘ㅅ’은 된소리로 발음함.)
            #print(syllable.final in double_consonant_final)
            # print(syllable.final)
            if syllable.final in double_consonant_final:
                double_consonant = double_consonant_final[syllable.final]
                syllable.final = double_consonant[0]
                next_syllable.initial = next_syllable.final_to_initial(double_consonant[1])
        return self._syllables

    
class Romanizer(object):
    def __init__(self, text):
        self.text = text

    def romanize(self):
        pronounced = Pronouncer(self.text).pronounced
        hangul = r"[가-힣ㄱ-ㅣ]"
        _romanized = ""
        for char in pronounced:
            if (re.match(hangul, char)):
                s = Syllable(char)
                #try:
                _romanized += onset[s.initial] + vowel[s.medial] + coda[s.final]
                #except Exception as e:
                #    _romanized += "[에러:" + str(e) + "]"
            else:
                _romanized += char

        return _romanized