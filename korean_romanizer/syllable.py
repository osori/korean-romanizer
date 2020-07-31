unicode_initial = [ 'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
unicode_initial = [ chr(initial_code) for initial_code in range(4352, 4371)]
unicode_medial = [ 'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']

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
        else:
            initial = ord(char)
            medial = None
            final = None
            
        return self.is_hangul(char), [initial, medial, final]
    
    def construct_syllable(self, initial, medial, final):
        if self.is_hangul(self.char):
            initial = ord(initial) - 4352
            medial = unicode_medial.index(medial)
            if final is None:
                final = 0
            else:
                final = unicode_final.index(final)
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
