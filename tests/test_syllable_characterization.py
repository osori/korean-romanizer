from korean_romanizer.syllable import Syllable


# Characterization tests for existing compatibility behavior, not desired future
# semantics. These lock down current reconstruction side effects before changing
# Syllable mutation behavior.


def test_repr_reconstructs_and_mutates_char_when_final_is_removed_current_behavior():
    syllable = Syllable("각")
    syllable.final = None

    assert syllable.char == "각"
    assert repr(syllable) == "가"
    assert syllable.char == "가"


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


def test_component_changes_are_used_for_reconstruction_current_behavior():
    syllable = Syllable("각")
    replacement = Syllable("동")
    syllable.initial = replacement.initial
    syllable.medial = replacement.medial
    syllable.final = replacement.final

    assert repr(syllable) == "동"
    assert syllable.char == "동"


def test_repeated_repr_and_str_calls_after_reconstruction_current_behavior():
    syllable = Syllable("각")
    syllable.final = None

    assert repr(syllable) == "가"
    assert repr(syllable) == "가"
    assert str(syllable) == "가"
    assert str(syllable) == "가"
    assert syllable.char == "가"


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
