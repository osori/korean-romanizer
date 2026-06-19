from korean_romanizer.syllable import Syllable

double_consonant_final = {
    'ᆪ': ('ᆨ', 'ᆺ'),
    'ᆬ': ('ᆫ', 'ᆽ'),
    'ᆭ': ('ᆫ', 'ᇂ'),
    'ᆰ': ('ᆯ', 'ᆨ'),
    'ᆱ': ('ᆯ', 'ᆷ'),
    'ᆲ': ('ᆯ', 'ᆸ'),
    'ᆳ': ('ᆯ', 'ᆻ'),
    'ᆴ': ('ᆯ', 'ᇀ'),
    'ᆵ': ('ᆯ', 'ᇁ'),
    'ᆶ': ('ᆯ', 'ᇂ'),
    'ᆹ': ('ᆸ', 'ᆺ'),
    'ㅆ': ('ㅅ', 'ㅅ')
}

NULL_CONSONANT = 'ᄋ'
INITIAL_CH = 'ᄎ'
INITIAL_H = 'ᄒ'
INITIAL_J = 'ᄌ'
INITIAL_N = 'ᄂ'
INITIAL_P = 'ᄑ'
INITIAL_RIEUL = 'ᄅ'
FINAL_D = 'ᆮ'
FINAL_K = 'ᆨ'
FINAL_M = 'ᆷ'
FINAL_N = 'ᆫ'
FINAL_NG = 'ᆼ'
FINAL_P = 'ᆸ'
FINAL_RIEUL = 'ᆯ'
FINAL_RIEUL_T = 'ᆴ'
FINAL_T = 'ᇀ'
MEDIAL_I = 'ㅣ'
MEDIAL_YEO = 'ㅕ'

PALATALIZED_BEFORE_I_BY_FINAL = {
    FINAL_D: (None, INITIAL_J),
    FINAL_T: (None, INITIAL_CH),
    FINAL_RIEUL_T: (FINAL_RIEUL, INITIAL_CH),
}

PALATALIZED_BEFORE_HI_BY_FINAL = {
    FINAL_D: (None, INITIAL_CH),
}

ASPIRATED_BEFORE_H_BY_FINAL = {
    FINAL_P: INITIAL_P,
}

# Standard Pronunciation Rule Article 19: initial ㄹ is pronounced ㄴ after
# ㄱ, ㅁ, ㅂ, and ㅇ; ㄱ and ㅂ also nasalize before the resulting ㄴ.
FINAL_BEFORE_RIEUL_TO_PRONOUNCED_FINAL = {
    FINAL_K: FINAL_NG,
    FINAL_M: FINAL_M,
    FINAL_NG: FINAL_NG,
    FINAL_P: FINAL_M,
}

# RR Special Provision 5 preserves administrative units such as 리 as "ri";
# assimilated sound changes before or after that boundary are not transcribed.
# This project does not yet emit proper-name capitalization or admin-unit
# hyphens, so this table only protects source-backed examples in the current
# lowercase/no-hyphen style.
RR_ADMIN_UNIT_RI_WORDS = (
    '인왕리',
)

# Standard Pronunciation Rule Article 20 exceptions where ㄴ+ㄹ is pronounced
# ㄴ+ㄴ, not ㄹ+ㄹ. 신문로 is an official RR adjacent-assimilation example.
N_R_TO_N_BOUNDARY_WORDS = (
    '의견란',
    '임진란',
    '생산량',
    '결단력',
    '공권력',
    '동원령',
    '상견례',
    '횡단로',
    '이원론',
    '입원료',
    '구근류',
    '신문로',
)

# Standard Pronunciation Rule Article 17 applies ㄷ/ㅌ palatalization before
# the vowel ㅣ only in particle/suffix contexts. Keep this list source-backed
# instead of applying a context-free ㄷ/ㅌ + 이 rule.
PALATALIZATION_BOUNDARY_WORDS = (
    '해돋이',
    '같이',
    '굳히다',
    '곧이듣다',
    '굳이',
    '미닫이',
    '땀받이',
    '밭이',
    '벼훑이',
    '닫히다',
    '묻히다',
)

# RR transcribes pronounced aspiration around ㅎ for source-backed examples such
# as 잡혀[자펴]. The same 잡- + -히/-혀- boundary appears in inflected forms
# such as 잡힌, 잡히다, 잡혔다, and 잡혔어.
#
# Keep this explicit instead of applying every ㄱ/ㄷ/ㅂ+ㅎ boundary, because RR
# does not transcribe the aspirated sound in noun examples such as 묵호 and 집현전.
H_ASPIRATION_BOUNDARY_PATTERNS = (
    ('잡', (MEDIAL_I, MEDIAL_YEO)),
)


def _find_n_r_to_n_boundaries(text):
    boundaries = set()

    for word in N_R_TO_N_BOUNDARY_WORDS:
        start = text.find(word)
        while start != -1:
            for offset in range(len(word) - 1):
                syllable = Syllable(word[offset])
                next_syllable = Syllable(word[offset + 1])
                if (
                    syllable.final == FINAL_N
                    and next_syllable.initial == INITIAL_RIEUL
                ):
                    boundaries.add(start + offset)

            start = text.find(word, start + 1)

    return boundaries


def _find_h_aspiration_boundaries(text):
    boundaries = set()

    for idx in range(len(text) - 1):
        for stem_syllable, next_medials in H_ASPIRATION_BOUNDARY_PATTERNS:
            if text[idx] != stem_syllable:
                continue

            syllable = Syllable(text[idx])
            next_syllable = Syllable(text[idx + 1])
            if (
                syllable.final in ASPIRATED_BEFORE_H_BY_FINAL
                and next_syllable.initial == INITIAL_H
                and next_syllable.medial in next_medials
            ):
                boundaries.add(idx)
                break

    return boundaries


def _find_palatalization_boundaries(text):
    boundaries = set()

    for word in PALATALIZATION_BOUNDARY_WORDS:
        start = text.find(word)
        while start != -1:
            for offset in range(len(word) - 1):
                syllable = Syllable(word[offset])
                next_syllable = Syllable(word[offset + 1])

                if next_syllable.medial != MEDIAL_I:
                    continue

                if (
                    next_syllable.initial == NULL_CONSONANT
                    and syllable.final in PALATALIZED_BEFORE_I_BY_FINAL
                ):
                    boundaries.add(start + offset)
                elif (
                    next_syllable.initial == INITIAL_H
                    and syllable.final in PALATALIZED_BEFORE_HI_BY_FINAL
                ):
                    boundaries.add(start + offset)

            start = text.find(word, start + 1)

    return boundaries


def _find_rieul_assimilation_preserved_boundaries(text):
    boundaries = set()

    for word in RR_ADMIN_UNIT_RI_WORDS:
        start = text.find(word)
        while start != -1:
            boundaries.add(start + len(word) - 2)
            start = text.find(word, start + 1)

    return boundaries


def _apply_representative_final(
    syllable,
    *,
    is_last_syllable,
    final_is_before_consonant,
):
    # 1. 받침 ‘ㄲ, ㅋ’, ‘ㅅ, ㅆ, ㅈ, ㅊ, ㅌ’, ‘ㅍ’은 어말 또는 자음 앞에서 각각 대표음 [ㄱ, ㄷ, ㅂ]으로 발음한다.
    # 2. 겹받침 ‘ㄳ’, ‘ㄵ’, ‘ㄼ, ㄽ, ㄾ’, ‘ㅄ’은 어말 또는 자음 앞에서 각각 [ㄱ, ㄴ, ㄹ, ㅂ]으로 발음한다.
    # 3. 겹받침 ‘ㄺ, ㄻ, ㄿ’은 어말 또는 자음 앞에서 각각 [ㄱ, ㅁ, ㅂ]으로 발음한다.
    # <-> 단, 국어의 로마자 표기법 규정에 의해 된소리되기는 표기에 반영하지 않으므로 제외.
    if is_last_syllable or final_is_before_consonant:
        if (syllable.final in ['ᆩ', 'ᆿ', 'ᆪ', 'ᆰ']):
            syllable.final = 'ᆨ'
        elif (syllable.final in ['ᆺ', 'ᆻ', 'ᆽ', 'ᆾ', 'ᇀ']):
            syllable.final = 'ᆮ'
        elif (syllable.final in ['ᇁ', 'ᆹ', 'ᆵ']):
            syllable.final = 'ᆸ'
        elif (syllable.final in ['ᆬ']):
            syllable.final = 'ᆫ'
        elif (syllable.final in ['ᆲ', 'ᆳ', 'ᆴ']):
            syllable.final = 'ᆯ'
        elif (syllable.final in ['ᆱ']):
            syllable.final = 'ᆷ'


def _apply_palatalization(syllable, next_syllable):
    if next_syllable.medial != MEDIAL_I:
        return

    if next_syllable.initial == NULL_CONSONANT:
        replacement = PALATALIZED_BEFORE_I_BY_FINAL.get(syllable.final)
    elif next_syllable.initial == INITIAL_H:
        replacement = PALATALIZED_BEFORE_HI_BY_FINAL.get(syllable.final)
    else:
        replacement = None

    if replacement:
        syllable.final, next_syllable.initial = replacement


def _apply_final_h_rules(syllable, next_syllable):
    # 4. 받침 ‘ㅎ’의 발음은 다음과 같다.
    if syllable.final in ['ᇂ', 'ᆭ', 'ᆶ']:
        without_ㅎ = {
            'ᆭ': 'ᆫ',
            'ᆶ': 'ᆯ',
            'ᇂ': None
        }

        if next_syllable:
            # ‘ㅎ(ㄶ, ㅀ)’ 뒤에 ‘ㄱ, ㄷ, ㅈ’이 결합되는 경우에는, 뒤 음절 첫소리와 합쳐서 [ㅋ, ㅌ, ㅊ]으로 발음한다.
            # ‘ㅎ(ㄶ, ㅀ)’ 뒤에 ‘ㅅ’이 결합되는 경우에는, ‘ㅅ’을 [ㅆ]으로 발음한다.
            if next_syllable.initial in ['ᄀ', 'ᄃ', 'ᄌ', 'ᄉ']:
                change_to = {'ᄀ': 'ᄏ', 'ᄃ': 'ᄐ', 'ᄌ': 'ᄎ', 'ᄉ': 'ᄊ'}
                syllable.final = without_ㅎ[syllable.final]
                next_syllable.initial = change_to[next_syllable.initial]
            # 3. ‘ㅎ’ 뒤에 ‘ㄴ’이 결합되는 경우에는, [ㄴ]으로 발음한다.
            elif next_syllable.initial in ['ᄂ']:
                # TODO: [붙임] ‘ㄶ, ㅀ’ 뒤에 ‘ㄴ’이 결합되는 경우에는, ‘ㅎ’을 발음하지 않는다.
                if (syllable.final in ['ᆭ', 'ᆶ']):
                    syllable.final = without_ㅎ[syllable.final]
                else:
                    syllable.final = 'ᆫ'
            # 4. ‘ㅎ(ㄶ, ㅀ)’ 뒤에 모음으로 시작된 어미나 접미사가 결합되는 경우에는,
            # ‘ㅎ’을 발음하지 않는다.
            elif next_syllable.initial == NULL_CONSONANT:
                if (syllable.final in ['ᆭ', 'ᆶ']):
                    if syllable.final == 'ᆭ':
                        syllable.final = 'ᆫ'
                    elif syllable.final == 'ᆶ':
                        syllable.final = 'ᆯ'
                else:
                    syllable.final = None
            elif next_syllable.initial == 'ᄅ':
                if (syllable.final == 'ᆶ'):
                    syllable.final = 'ᆯ'
            else:
                if (syllable.final == 'ᇂ'):
                    syllable.final = None
        else:
            syllable.final = without_ㅎ[syllable.final]


def _apply_h_aspiration(syllable, next_syllable):
    aspirated_initial = ASPIRATED_BEFORE_H_BY_FINAL.get(syllable.final)
    if aspirated_initial and next_syllable.initial == INITIAL_H:
        syllable.final = None
        next_syllable.initial = aspirated_initial


def _apply_double_final_linking(syllable, next_syllable):
    # 6. 겹받침이 모음으로 시작된 조사나 어미, 접미사와 결합되는 경우에는,
    # 뒤엣것만을 뒤 음절 첫소리로 옮겨 발음한다.(이 경우, ‘ㅅ’은 된소리로 발음함.)
    if syllable.final in double_consonant_final and next_syllable.initial == NULL_CONSONANT:
        double_consonant = double_consonant_final[syllable.final]
        syllable.final = double_consonant[0]
        next_syllable.initial = next_syllable.final_to_initial(
            double_consonant[1])


class Pronouncer(object):
    """Apply Korean pronunciation substitutions before romanization."""

    def __init__(self, text):
        self._h_aspiration_boundaries = _find_h_aspiration_boundaries(text)
        self._n_r_to_n_boundaries = _find_n_r_to_n_boundaries(text)
        self._palatalization_boundaries = _find_palatalization_boundaries(text)
        self._rieul_assimilation_preserved_boundaries = (
            _find_rieul_assimilation_preserved_boundaries(text))
        self._syllables = [Syllable(char) for char in text]
        self.pronounced = ''.join([str(c) for c in self.final_substitute()])

    def final_substitute(self):
        for idx, syllable in enumerate(self._syllables):
            try:
                next_syllable = self._syllables[idx+1]
            except IndexError:
                next_syllable = None

            try:
                final_is_before_C = syllable.final and next_syllable.initial not in (
                    None, NULL_CONSONANT)
            except AttributeError:
                final_is_before_C = False

            try:
                final_is_before_V = syllable.final and next_syllable.initial in (
                    None, NULL_CONSONANT)
            except AttributeError:
                final_is_before_V = False

            is_last_syllable = syllable.final and next_syllable is None

            _apply_representative_final(
                syllable,
                is_last_syllable=is_last_syllable,
                final_is_before_consonant=final_is_before_C,
            )

            _apply_final_h_rules(syllable, next_syllable)

            # RR transcribes source-backed ㅎ aspiration, e.g. 잡혀[자펴],
            # while preserving noun examples such as 묵호 and 집현전.
            if next_syllable and idx in self._h_aspiration_boundaries:
                _apply_h_aspiration(syllable, next_syllable)

            # Revised Romanization follows pronounced palatalization, e.g.
            # 해돋이[해도지], 같이[가치], 굳히다[구치다].
            if next_syllable and idx in self._palatalization_boundaries:
                _apply_palatalization(syllable, next_syllable)

            _apply_double_final_linking(syllable, next_syllable)

            # Revised Romanization follows pronounced forms for adjacent liquids
            # and nasals, e.g. 종로[종노], 왕십리[왕심니], 신라[실라],
            # 별내[별래].
            if next_syllable:
                if (
                    next_syllable.initial == INITIAL_RIEUL
                    and idx not in self._rieul_assimilation_preserved_boundaries
                ):
                    pronounced_final = FINAL_BEFORE_RIEUL_TO_PRONOUNCED_FINAL.get(
                        syllable.final)
                    if pronounced_final:
                        syllable.final = pronounced_final
                        next_syllable.initial = INITIAL_N
                    elif syllable.final == FINAL_N:
                        if idx in self._n_r_to_n_boundaries:
                            next_syllable.initial = INITIAL_N
                        else:
                            syllable.final = FINAL_RIEUL
                elif (
                    syllable.final == FINAL_RIEUL
                    and next_syllable.initial == INITIAL_N
                ):
                    next_syllable.initial = INITIAL_RIEUL
                    
            # 5. 홑받침이나 쌍받침이 모음으로 시작된 조사나 어미, 접미사와 결합되는 경우에는,
            # 제 음가대로 뒤 음절 첫소리로 옮겨 발음한다.
            if next_syllable and final_is_before_V:
                # do nothing if final is ᆼ or null
                if (next_syllable.initial == NULL_CONSONANT and syllable.final not in ["ᆼ", None]):
                    next_syllable.initial = next_syllable.final_to_initial(
                        syllable.final)
                    syllable.final = None

        return self._syllables
