import pytest
from korean_romanizer.romanizer import Romanizer


def romanize(text):
    r = Romanizer(text)
    return r.romanize()


def test_simple():
    assert romanize("안녕하세요") == "annyeonghaseyo"


def test_spaced_text():
    assert romanize("아이유 방탄소년단") == "aiyu bangtansonyeondan"


def test_onset_g_d_b():
    assert romanize("구미") == "gumi"
    assert romanize("영동") == "yeongdong"
    assert romanize("한밭") == "hanbat"


def test_coda_g_d_b():
    assert romanize("밝다") == "bakda"
    assert romanize("바닷가") == "badatga"
    assert romanize("없다") == "eopda"
    assert romanize("앞만") == "apman"
    assert romanize("읊다") == "eupda"


def test_r_l():
    assert romanize("구리") == "guri"
    assert romanize("설악") == "seorak"
#    assert romanize("울릉") == "ulleung"
#    assert romanize("대관령") == "daegwallyeong"


def test_next_syllable_null_initial():
    assert romanize("강약") == "gangyak"
    assert romanize("강원") == "gangwon"
    assert romanize("좋아하고") == "joahago"
    assert romanize("좋은") == "joeun"


def test_double_consonant_final_and_next_syllable_null_initial():
    assert romanize("했었어요") == "haesseosseoyo"
    assert romanize("없었다") == "eopseotda"
    assert romanize("앉아봐") == "anjabwa"
    assert romanize("닭의") == "dalgui"
    assert romanize("밟아") == "balba"
    assert romanize("닮았네") == "dalmatne"
    assert romanize("삯을") == "sakseul"
    assert romanize("앓았다") == "aratda"
    assert romanize("읊어 보거라") == "eulpeo bogeora"
    assert romanize("곬이") == "golssi"
    assert romanize("훑어보다") == "hulteoboda"


def test_double_consonant_final_and_next_syllable_not_null_initial():
    assert romanize("앉고싶다") == "angosipda"
    assert romanize("뚫리다") == "ttulrida"
    assert romanize("칡뿌리") == "chikppuri"
    

def test_double_consonant_final_without_next_syllable():
    assert romanize("괜찮") == "gwaenchan"
    assert romanize("뚫") == "ttul"
    assert romanize("않") == "an"


def test_non_syllables():
    assert romanize("ㅠㄴㅁㄱ") == "yunmg"
    assert romanize("ㅠ동") == "yudong"


def test_coda_h():
    assert romanize("않습니다") == "ansseupnida"
    assert romanize("앓고") == "alko"
