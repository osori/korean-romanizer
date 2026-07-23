import pytest

from korean_romanizer.pronouncer import Pronouncer, _apply_final_h_rules
from korean_romanizer.romanizer import Romanizer, romanize
from korean_romanizer.syllable import Syllable, unicode_final
from korean_romanizer.tables import coda


INITIAL_COUNT = 19
MEDIAL_COUNT = 21
FINAL_COUNT = 28
H_BEARING_FINALS = ("ᆭ", "ᆶ", "ᇂ")
BOUNDARY_FOLLOWERS = (
    "",
    " ",
    "\t",
    "\n",
    "!",
    "A",
    "7",
    "🙂",
    "ㄹ",
    "ㅏ",
    "ᄅ",
    "ᅡ",
)


def _syllable(*, initial_index=0, medial_index=0, final_index=0):
    return chr(
        0xAC00
        + initial_index * MEDIAL_COUNT * FINAL_COUNT
        + medial_index * FINAL_COUNT
        + final_index
    )


OPEN_HANGUL_FOLLOWERS = tuple(
    _syllable(initial_index=initial_index, medial_index=medial_index)
    for initial_index in range(INITIAL_COUNT)
    for medial_index in range(MEDIAL_COUNT)
)


@pytest.mark.parametrize(
    ("text", "pronounced", "expected"),
    [
        ("않 ", "안 ", "an "),
        ("많!", "만!", "man!"),
        ("싫?", "실?", "sil?"),
    ],
)
def test_final_h_family_reduces_at_non_syllable_boundaries(
    text,
    pronounced,
    expected,
):
    # NIKL final-consonant guidance reduces ㄶ/ㅀ at a boundary to ㄴ/ㄹ.
    # The library contract preserves the following separator or punctuation.
    # See https://www.korean.go.kr/nkview/nklife/1993_1/3_1.html.
    assert Pronouncer(text).pronounced == pronounced
    assert romanize(text) == expected
    assert Romanizer(text).romanize() == expected


@pytest.mark.parametrize("final", H_BEARING_FINALS)
def test_final_h_rule_always_leaves_a_romanizable_coda(final):
    current = Syllable(_syllable(final_index=unicode_final.index(final)))
    followers = OPEN_HANGUL_FOLLOWERS + BOUNDARY_FOLLOWERS

    failures = []
    for follower in followers:
        candidate = Syllable(str(current))
        next_syllable = Syllable(follower) if follower else None
        _apply_final_h_rules(candidate, next_syllable)
        if candidate.final not in coda:
            failures.append((follower, candidate.final))

    assert failures == []


@pytest.mark.parametrize("final_index", range(FINAL_COUNT))
def test_romanize_returns_a_string_for_every_coda_and_boundary_combination(
    final_index,
):
    followers = OPEN_HANGUL_FOLLOWERS + BOUNDARY_FOLLOWERS
    failures = []

    current = _syllable(final_index=final_index)
    for follower in followers:
        text = current + follower
        try:
            result = romanize(text)
        except Exception as error:
            failures.append((text, type(error).__name__, str(error)))
        else:
            if not isinstance(result, str):
                failures.append((text, type(result).__name__, result))

    assert failures == []
