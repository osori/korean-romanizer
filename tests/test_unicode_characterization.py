"""Characterize current Unicode normalization behavior.

These fixtures document observed behavior only. They are not desired-behavior
claims and are not intended to provide complete Revised Romanization coverage.
"""

import unicodedata

from korean_romanizer import romanize


def test_nfc_precomposed_hangul_romanizes_current_behavior():
    text = unicodedata.normalize(
        "NFC",
        "\u110b\u1161\u11ab\u1102\u1167\u11bc",
    )

    assert text == "\uc548\ub155"
    assert romanize(text) == "annyeong"


def test_equivalent_nfd_hangul_passes_through_current_behavior():
    nfc_text = unicodedata.normalize(
        "NFC",
        "\u110b\u1161\u11ab\u1102\u1167\u11bc",
    )
    text = unicodedata.normalize("NFD", nfc_text)

    assert unicodedata.normalize("NFC", text) == nfc_text
    assert romanize(text) == text


def test_modern_decomposed_choseong_jungseong_jongseong_current_behavior():
    text = unicodedata.normalize("NFD", "\uac01")

    assert text == "\u1100\u1161\u11a8"
    assert unicodedata.normalize("NFC", text) == "\uac01"
    assert romanize(text) == text


def test_representative_compatibility_jamo_current_behavior():
    compatibility_jamo = unicodedata.normalize("NFC", "\u3131")
    compatibility_decomposed = unicodedata.normalize("NFKD", compatibility_jamo)

    assert compatibility_jamo == "\u3131"
    assert romanize(compatibility_jamo) == "g"
    assert compatibility_decomposed == "\u1100"
    assert romanize(compatibility_decomposed) == compatibility_decomposed


def test_mixed_nfc_nfd_korean_and_non_korean_text_current_behavior():
    nfc_hangul = unicodedata.normalize("NFC", "\u110b\u1161\u11ab")
    nfd_hangul = unicodedata.normalize("NFD", "\ub155")
    text = f"ID:{nfc_hangul}/{nfd_hangul}/ABC"

    assert romanize(text) == f"ID:an/{nfd_hangul}/ABC"


def test_punctuation_and_whitespace_preservation_current_behavior():
    nfc_hangul = unicodedata.normalize("NFC", "\u1100\u116e\u1106\u1175")
    nfd_hangul = unicodedata.normalize("NFD", "\uc11c\uc6b8")
    text = f"  {nfc_hangul},\t{nfd_hangul}!\n"

    assert romanize(text) == f"  gumi,\t{nfd_hangul}!\n"


def test_unsupported_archaic_jamo_pass_through_current_behavior():
    text = unicodedata.normalize("NFC", "\u1159\u119e")

    assert [unicodedata.name(char) for char in text] == [
        "HANGUL CHOSEONG YEORINHIEUH",
        "HANGUL JUNGSEONG ARAEA",
    ]
    assert romanize(text) == text
