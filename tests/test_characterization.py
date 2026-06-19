import pytest

from korean_romanizer import romanizer, syllable, tables
from korean_romanizer.pronouncer import Pronouncer
from korean_romanizer.romanizer import Romanizer
from korean_romanizer.syllable import Syllable


def romanize(text):
    return Romanizer(text).romanize()


def test_romanizer_table_imports_current_behavior():
    assert romanizer.vowel is tables.vowel
    assert romanizer.onset is tables.onset
    assert romanizer.coda is tables.coda
    assert romanizer.compat_onset is tables.compat_onset
    assert romanizer.unicode_initial is syllable.unicode_initial
    assert romanizer.unicode_compatible_consonants is syllable.unicode_compatible_consonants


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello, 안녕? 123", "Hello, annyeong? 123"),
        ("구미,\t영동   서울!!", "gumi,\tyeongdong   seoul!!"),
        ("  안녕\n하세요  ", "  annyeong\nhaseyo  "),
    ],
)
def test_preserves_non_hangul_boundaries_current_behavior(text, expected):
    assert romanize(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("가", "가"),
        ("ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ", "gkkndttrmbppsssjjjchktph"),
        ("ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ", "aaeyayaeeoeyeoyeowawaeoeyouwowewiyueuuii"),
    ],
)
def test_jamo_current_behavior(text, expected):
    assert romanize(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("좋습니다", "josseupnida"),
        ("놓고", "noko"),
        ("닿지", "dachi"),
        ("많소", "mansso"),
        ("좋니", "jonni"),
        ("닿는", "danneun"),
        ("놓아", "noa"),
        ("낳은", "naeun"),
        ("싫어", "sireo"),
        ("앉히다", "anhida"),
        ("넋없다", "neokseopda"),
        ("값있는", "gapsitneun"),
        ("외곬으로", "oegolsseuro"),
    ],
)
def test_final_consonant_rules_current_behavior(text, expected):
    assert romanize(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("좋습니다", "조씁니다"),
        ("넋없다", "넉섭다"),
        ("값있는", "갑싣는"),
        ("외곬으로", "외골쓰로"),
        ("구미,\t영동", "구미,\t영동"),
    ],
)
def test_pronouncer_current_behavior(text, expected):
    assert Pronouncer(text).pronounced == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("놓고", "노코"),
        ("놓다", "노타"),
        ("낳지", "나치"),
        ("많소", "만쏘"),
        ("좋니", "존니"),
        ("닿는", "단는"),
        ("놓아", "노아"),
        ("낳은", "나은"),
        ("싫어", "시러"),
        ("뚫리다", "뚤리다"),
        ("좋", "조"),
        ("않", "안"),
        ("앓", "알"),
    ],
)
def test_final_h_rules_current_behavior(text, expected):
    # Characterize preserved final-ㅎ pronunciation behavior, not RR claims.
    assert Pronouncer(text).pronounced == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("부엌", "부억"),
        ("옷", "옫"),
        ("앞", "압"),
        ("넋", "넉"),
        ("앉", "안"),
        ("핥", "할"),
        ("삶", "삼"),
    ],
)
def test_representative_final_reduction_at_word_end_current_behavior(text, expected):
    assert Pronouncer(text).pronounced == expected


def test_representative_final_reduction_before_consonant_current_behavior():
    assert Pronouncer("부엌문").pronounced == "부억문"


def test_representative_final_preserves_vowel_linking_current_behavior():
    assert Pronouncer("부엌에").pronounced == "부어케"


@pytest.mark.parametrize(
    ("char", "expected"),
    [
        ("각", ("ᄀ", "ㅏ", "ᆨ", "각")),
        ("가", ("ᄀ", "ㅏ", None, "가")),
        ("A", (65, None, None, "A")),
        ("ㄱ", (12593, None, None, "ㄱ")),
    ],
)
def test_syllable_decomposition_current_behavior(char, expected):
    syllable = Syllable(char)

    assert (syllable.initial, syllable.medial, syllable.final, str(syllable)) == expected


@pytest.mark.parametrize(
    ("final", "initial"),
    [
        ("ᆨ", "ᄀ"),
        ("ᆺ", "ᄉ"),
        ("ᆽ", "ᄌ"),
        ("ᇂ", "ᄒ"),
    ],
)
def test_syllable_final_to_initial_current_behavior(final, initial):
    assert Syllable("각").final_to_initial(final) == initial
