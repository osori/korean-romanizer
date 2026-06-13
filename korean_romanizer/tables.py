"""
Hangul romanization tables and Unicode constants.

This module is a pure data leaf — no project-internal imports.
All romanization lookup tables and Unicode structural data live here.
"""

# ─── Unicode structural constants ────────────────────────────────────────────

unicode_initial = [chr(initial_code) for initial_code in range(4352, 4371)]
unicode_medial = [
    'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ',
    'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ',
    'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ',
]
unicode_final = [chr(final_code) for final_code in range(0x11A8, 0x11C3)]
unicode_final.insert(0, None)

unicode_offset = 44032
unicode_initial_offset = 588
unicode_medial_offset = 28

unicode_compatible_consonants = [
    'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ',
    'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ',
    'ㅌ', 'ㅍ', 'ㅎ',
]
unicode_compatible_finals = [
    'ᆨ', 'ᆩ', 'ᆫ', 'ᆮ', '_', 'ᆯ', 'ᆷ', 'ᆸ',
    '_', 'ᆺ', 'ᆻ', 'ᆼ', 'ᆽ', '_', 'ᆾ', 'ᆿ',
    'ᇀ', 'ᇁ', 'ᇂ',
]

# The null consonant (ㅇ in initial position = silent)
NULL_CONSONANT = 'ᄋ'

# ─── Vowel romanization (Jungseong → Latin) ─────────────────────────────────

VOWEL_ROMANIZATION = {
    # 단모음 monophthongs
    'ㅏ': 'a',
    'ㅓ': 'eo',
    'ㅗ': 'o',
    'ㅜ': 'u',
    'ㅡ': 'eu',
    'ㅣ': 'i',
    'ㅐ': 'ae',
    'ㅔ': 'e',
    'ㅚ': 'oe',
    'ㅟ': 'wi',

    # 이중모음 diphthongs
    'ㅑ': 'ya',
    'ㅕ': 'yeo',
    'ㅛ': 'yo',
    'ㅠ': 'yu',
    'ㅒ': 'yae',
    'ㅖ': 'ye',
    'ㅘ': 'wa',
    'ㅙ': 'wae',
    'ㅝ': 'wo',
    'ㅞ': 'we',
    'ㅢ': 'ui',  # [붙임 1] 'ㅢ'는 'ㅣ'로 소리 나더라도 'ui'로 적는다.
}

# ─── Onset romanization (Choseong → Latin) ──────────────────────────────────

ONSET_ROMANIZATION = {
    # 파열음 stops/plosives
    'ᄀ': 'g',
    'ᄁ': 'kk',
    'ᄏ': 'k',
    'ᄃ': 'd',
    'ᄄ': 'tt',
    'ᄐ': 't',
    'ᄇ': 'b',
    'ᄈ': 'pp',
    'ᄑ': 'p',
    # 파찰음 affricates
    'ᄌ': 'j',
    'ᄍ': 'jj',
    'ᄎ': 'ch',
    # 마찰음 fricatives
    'ᄉ': 's',
    'ᄊ': 'ss',
    'ᄒ': 'h',
    # 비음 nasals
    'ᄂ': 'n',
    'ᄆ': 'm',
    # 유음 liquids
    'ᄅ': 'r',
    # Null sound
    'ᄋ': '',
}

# ─── Coda romanization (Jongseong → Latin) ──────────────────────────────────

CODA_ROMANIZATION = {
    # 파열음 stops/plosives
    'ᆨ': 'k',
    'ᆮ': 't',
    'ᆸ': 'p',
    # 비음 nasals
    'ᆫ': 'n',
    'ᆼ': 'ng',
    'ᆷ': 'm',
    # 유음 liquids
    'ᆯ': 'l',
    None: '',
}

# Compatibility jamo (e.g. ㄱ, ㄴ) do not appear as part of a full syllable.
# Map them to their onset romanization so single jamo can be transliterated.
COMPAT_ONSET_ROMANIZATION = {
    comp: ONSET_ROMANIZATION[unicode_initial[i]]
    for i, comp in enumerate(unicode_compatible_consonants)
}

# ─── Pronunciation rule data ────────────────────────────────────────────────

# Double consonant final decomposition: 겹받침 → (first coda, second coda)
DOUBLE_CONSONANT_FINAL = {
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
    'ㅆ': ('ㅅ', 'ㅅ'),
}

# Representative sound mapping: complex codas → representative sound
# Rules 1-3: 받침 'ㄲ, ㅋ', 'ㅅ, ㅆ, ㅈ, ㅊ, ㅌ', 'ㅍ' → [ㄱ, ㄷ, ㅂ]
# 겹받침 'ㄳ', 'ㄵ', 'ㄼ, ㄽ, ㄾ', 'ㅄ' → [ㄱ, ㄴ, ㄹ, ㅂ]
# 겹받침 'ㄺ, ㄻ, ㄿ' → [ㄱ, ㅁ, ㅂ]
REPRESENTATIVE_SOUND = {
    # → ㄱ (k)
    'ᆩ': 'ᆨ', 'ᆿ': 'ᆨ', 'ᆪ': 'ᆨ', 'ᆰ': 'ᆨ',
    # → ㄷ (t)
    'ᆺ': 'ᆮ', 'ᆻ': 'ᆮ', 'ᆽ': 'ᆮ', 'ᆾ': 'ᆮ', 'ᇀ': 'ᆮ',
    # → ㅂ (p)
    'ᇁ': 'ᆸ', 'ᆹ': 'ᆸ', 'ᆵ': 'ᆸ',
    # → ㄴ (n)
    'ᆬ': 'ᆫ',
    # → ㄹ (l)
    'ᆲ': 'ᆯ', 'ᆳ': 'ᆯ', 'ᆴ': 'ᆯ',
    # → ㅁ (m)
    'ᆱ': 'ᆷ',
}

# ㅎ final mapping: which coda remains after removing ㅎ
WITHOUT_H_FINAL = {
    'ᆭ': 'ᆫ',
    'ᆶ': 'ᆯ',
    'ᇂ': None,
}

# Aspiration mapping: ㅎ + ㄱ/ㄷ/ㅈ/ㅅ → ㅋ/ㅌ/ㅊ/ㅆ
ASPIRATION_MAP = {
    'ᄀ': 'ᄏ',
    'ᄃ': 'ᄐ',
    'ᄌ': 'ᄎ',
    'ᄉ': 'ᄊ',
}

# ─── Backward compatibility aliases ──────────────────────────────────────────
# These preserve the original public names so existing code continues to work.
# New code should use the UPPERCASE names directly.

vowel = VOWEL_ROMANIZATION
onset = ONSET_ROMANIZATION
coda = CODA_ROMANIZATION
compat_onset = COMPAT_ONSET_ROMANIZATION
