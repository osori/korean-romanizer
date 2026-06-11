import pytest

from korean_romanizer.pronouncer import Pronouncer
from korean_romanizer.romanizer import Romanizer


def romanize(text):
    return Romanizer(text).romanize()


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("종로", "jongno"),
        ("신라", "silla"),
        ("울릉", "ulleung"),
        ("대관령", "daegwallyeong"),
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
        ("종로", "종노"),
        ("신라", "실라"),
        ("대관령", "대괄령"),
        ("별내", "별래"),
    ],
)
def test_liquid_and_nasal_assimilation_pronunciation(text, expected):
    assert Pronouncer(text).pronounced == expected
