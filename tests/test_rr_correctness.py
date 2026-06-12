import pytest

from korean_romanizer.pronouncer import Pronouncer
from korean_romanizer.romanizer import Romanizer


def romanize(text):
    return Romanizer(text).romanize()


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("난로", "nallo"),
        ("종로", "jongno"),
        ("신라", "silla"),
        ("천리", "cheolli"),
        ("울릉", "ulleung"),
        ("광한루", "gwanghallu"),
        ("대관령", "daegwallyeong"),
        ("칼날", "kallal"),
        ("물난리", "mullalli"),
        ("별내", "byeollae"),
    ],
)
def test_liquid_and_nasal_assimilation_rr_correctness(text, expected):
    # Official NIKL RR examples include 종로[종노], 신라[실라],
    # 울릉, 대관령[대괄령], and 별내[별래].
    # See https://www.korean.go.kr/front_eng/roman/roman_01.do.
    assert romanize(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("의견란", "uigyeonnan"),
        ("임진란", "imjinnan"),
        ("생산량", "saengsannyang"),
        ("결단력", "gyeoldannyeok"),
        ("공권력", "gonggwonnyeok"),
        ("동원령", "dongwonnyeong"),
        ("상견례", "sanggyeonnye"),
        ("횡단로", "hoengdanno"),
        ("이원론", "iwonnon"),
        ("입원료", "ibwonnyo"),
        ("구근류", "gugeunnyu"),
        ("신문로", "sinmunno"),
    ],
)
def test_n_r_to_n_exception_rr_correctness(text, expected):
    # Standard Pronunciation Rule Article 20 lists cases where ㄴ+ㄹ
    # is pronounced ㄴ+ㄴ. Official RR also includes 신문로[신문노].
    assert romanize(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("난로", "날로"),
        ("종로", "종노"),
        ("신라", "실라"),
        ("천리", "철리"),
        ("광한루", "광할루"),
        ("대관령", "대괄령"),
        ("칼날", "칼랄"),
        ("물난리", "물랄리"),
        ("별내", "별래"),
    ],
)
def test_liquid_and_nasal_assimilation_pronunciation(text, expected):
    assert Pronouncer(text).pronounced == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("의견란", "의견난"),
        ("임진란", "임진난"),
        ("생산량", "생산냥"),
        ("결단력", "결단녁"),
        ("공권력", "공권녁"),
        ("동원령", "동원녕"),
        ("상견례", "상견녜"),
        ("횡단로", "횡단노"),
        ("이원론", "이원논"),
        ("입원료", "이붠뇨"),
        ("구근류", "구근뉴"),
        ("신문로", "신문노"),
    ],
)
def test_n_r_to_n_exception_pronunciation(text, expected):
    # This project intentionally avoids RR-irrelevant tensification, so these
    # expected pronunciations focus on the ㄹ-to-ㄴ boundary change.
    assert Pronouncer(text).pronounced == expected
