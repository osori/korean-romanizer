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
        ("강릉", "gangneung"),
        ("담력", "damnyeok"),
        ("막론", "mangnon"),
        ("석류", "seongnyu"),
        ("협력", "hyeomnyeok"),
        ("법리", "beomni"),
        ("십리", "simni"),
        ("왕십리", "wangsimni"),
    ],
)
def test_rieul_to_n_after_nasal_and_stop_codas_rr_correctness(text, expected):
    # Standard Pronunciation Rule Article 19 changes ㄹ to ㄴ after
    # ㄱ/ㅁ/ㅂ/ㅇ; ㄱ and ㅂ nasalize before that resulting ㄴ.
    # Official RR includes 왕십리[왕심니].
    assert romanize(text) == expected


def test_administrative_unit_ri_preserves_rr_spelling():
    # Official RR is Inwang-ri. This project currently omits proper-name
    # capitalization and administrative-unit hyphenation, so assert inwangri.
    assert romanize("인왕리") == "inwangri"
    assert romanize("왕십리") == "wangsimni"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("해돋이", "haedoji"),
        ("같이", "gachi"),
        ("굳히다", "guchida"),
        ("굳이", "guji"),
        ("밭이", "bachi"),
        ("벼훑이", "byeohulchi"),
    ],
)
def test_palatalization_rr_correctness(text, expected):
    # Official NIKL RR examples include 해돋이[해도지],
    # 같이[가치], and 굳히다[구치다].
    # See https://www.korean.go.kr/front_eng/roman/roman_01.do.
    assert romanize(text) == expected


def test_palatalization_does_not_apply_to_lexical_ieo():
    assert Pronouncer("곧이어").pronounced == "고디어"
    assert romanize("곧이어") == "godieo"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("좋고", "joko"),
        ("놓다", "nota"),
        ("잡혀", "japyeo"),
        ("낳지", "nachi"),
    ],
)
def test_h_adjacency_rr_correctness(text, expected):
    # Official NIKL RR examples include 좋고[조코], 놓다[노타],
    # 잡혀[자펴], and 낳지[나치].
    # See https://www.korean.go.kr/front_eng/roman/roman_01.do.
    assert romanize(text) == expected


@pytest.mark.parametrize(
    ("text", "pronounced", "expected"),
    [
        ("많고", "만코", "manko"),
        ("꿇리다", "꿀리다", "kkullida"),
    ],
)
def test_compound_final_h_at_sourced_hangul_boundaries_rr_correctness(
    text,
    pronounced,
    expected,
):
    # Standard Pronunciation Rule Article 12 gives 많고[만코]; the NIKL
    # Korean Basic Dictionary gives 꿇리다[꿀리다].
    # See https://www.korean.go.kr/kornorms/regltn/regltnView.do?regltn_code=0002&regltn_no=346
    # and https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=37901&nation=eng.
    assert Pronouncer(text).pronounced == pronounced
    assert romanize(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("잡혀", "japyeo"),
        ("잡히다", "japida"),
        ("잡힌", "japin"),
        ("잡혔다", "japyeotda"),
        ("잡혔어", "japyeosseo"),
    ],
)
def test_h_adjacency_japhida_inflections_rr_correctness(text, expected):
    assert romanize(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("묵호", "mukho"),
        ("집현전", "jiphyeonjeon"),
    ],
)
def test_h_adjacency_noun_examples_do_not_transcribe_aspiration(text, expected):
    # RR does not transcribe aspirated sounds in nouns where ㅎ follows
    # ㄱ, ㄷ, or ㅂ, as in official examples 묵호 and 집현전.
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


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("강릉", "강능"),
        ("담력", "담녁"),
        ("막론", "망논"),
        ("석류", "성뉴"),
        ("협력", "혐녁"),
        ("법리", "범니"),
        ("십리", "심니"),
        ("왕십리", "왕심니"),
    ],
)
def test_rieul_to_n_after_nasal_and_stop_codas_pronunciation(text, expected):
    assert Pronouncer(text).pronounced == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("해돋이", "해도지"),
        ("같이", "가치"),
        ("굳히다", "구치다"),
        ("굳이", "구지"),
        ("밭이", "바치"),
        ("벼훑이", "벼훌치"),
    ],
)
def test_palatalization_pronunciation(text, expected):
    assert Pronouncer(text).pronounced == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("좋고", "조코"),
        ("놓다", "노타"),
        ("잡혀", "자펴"),
        ("낳지", "나치"),
        ("묵호", "묵호"),
        ("집현전", "집현전"),
    ],
)
def test_h_adjacency_pronunciation(text, expected):
    assert Pronouncer(text).pronounced == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("잡혀", "자펴"),
        ("잡히다", "자피다"),
        ("잡힌", "자핀"),
    ],
)
def test_h_adjacency_japhida_inflections_pronunciation(text, expected):
    assert Pronouncer(text).pronounced == expected
