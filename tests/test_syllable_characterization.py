from korean_romanizer.syllable import Syllable


# Characterization tests for Syllable reconstruction side effects.


def test_repr_reconstructs_without_mutating_char_when_final_is_removed():
    syllable = Syllable("각")
    syllable.final = None

    assert syllable.char == "각"
    assert repr(syllable) == "가"
    assert syllable.char == "각"


def test_str_reconstructs_and_mutates_char_when_final_is_removed_current_behavior():
    syllable = Syllable("각")
    syllable.final = None

    assert syllable.char == "각"
    assert str(syllable) == "가"
    assert syllable.char == "가"


def test_construct_syllable_returns_reconstructed_char_and_mutates_char_current_behavior():
    syllable = Syllable("각")
    syllable.final = None

    assert syllable.construct_syllable(syllable.initial, syllable.medial, syllable.final) == "가"
    assert syllable.char == "가"


def test_repr_uses_component_changes_without_mutating_char():
    syllable = Syllable("각")
    replacement = Syllable("동")
    syllable.initial = replacement.initial
    syllable.medial = replacement.medial
    syllable.final = replacement.final

    assert repr(syllable) == "동"
    assert syllable.char == "각"


def test_repeated_repr_and_str_calls_show_only_str_mutates_char():
    repr_syllable = Syllable("각")
    repr_syllable.final = None

    assert repr(repr_syllable) == "가"
    assert repr(repr_syllable) == "가"
    assert repr_syllable.char == "각"

    str_syllable = Syllable("각")
    str_syllable.final = None

    assert str(str_syllable) == "가"
    assert str(str_syllable) == "가"
    assert str_syllable.char == "가"


def test_non_hangul_repr_and_str_preserve_existing_char_current_behavior():
    repr_syllable = Syllable("A")
    str_syllable = Syllable("A")

    assert repr(repr_syllable) == "A"
    assert repr_syllable.char == "A"
    assert str(str_syllable) == "A"
    assert str_syllable.char == "A"


def test_final_less_hangul_syllable_repr_and_str_current_behavior():
    repr_syllable = Syllable("가")
    str_syllable = Syllable("가")

    assert repr(repr_syllable) == "가"
    assert repr_syllable.char == "가"
    assert str(str_syllable) == "가"
    assert str_syllable.char == "가"


def test_hangul_syllable_with_final_consonant_repr_and_str_current_behavior():
    repr_syllable = Syllable("각")
    str_syllable = Syllable("각")

    assert repr(repr_syllable) == "각"
    assert repr_syllable.char == "각"
    assert str(str_syllable) == "각"
    assert str_syllable.char == "각"
