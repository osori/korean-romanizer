import korean_romanizer
from korean_romanizer import Pronouncer, Romanizer, Syllable, romanize
from korean_romanizer.romanizer import Romanizer as ModuleRomanizer
from korean_romanizer.romanizer import romanize as module_romanize


EXPECTED_ALL = (
    "romanize",
    "Romanizer",
    "Pronouncer",
    "Syllable",
)


def test_functional_api_output():
    assert romanize("안녕하세요") == "annyeonghaseyo"


def test_package_and_module_exports_are_identical():
    assert romanize is module_romanize
    assert Romanizer is ModuleRomanizer


def test_class_api_matches_function():
    text = "아이유 방탄소년단"
    assert Romanizer(text).romanize() == romanize(text)


def test_all_exports_exact_public_api():
    assert korean_romanizer.__all__ == EXPECTED_ALL


def test_wildcard_import_exports_only_public_api():
    namespace = {}

    exec("from korean_romanizer import *", namespace)

    exported = {name for name in namespace if not name.startswith("__")}
    assert exported == set(EXPECTED_ALL)
    assert namespace["romanize"] is romanize
    assert namespace["Romanizer"] is Romanizer
    assert namespace["Pronouncer"] is Pronouncer
    assert namespace["Syllable"] is Syllable


def test_lower_level_compatibility_exports_remain_importable():
    assert Pronouncer("안녕하세요").pronounced
    assert Syllable("한").char == "한"
