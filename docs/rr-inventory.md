# Bounded Revised Romanization Inventory

This inventory covers every displayed word- and name-level example on the
National Institute of Korean Language (NIKL)
[Romanization of Korean](https://www.korean.go.kr/front_eng/roman/roman_01.do)
page in the snapshot captured on 2026-07-23 and rechecked unchanged on
2026-07-24. It includes the examples in the Section 2 consonant notes and all
Section 3 provisions that show word or name examples. It excludes the base jamo
mapping rows, which existing table tests cover; Section 3(7), which shows no
examples; and any examples from supporting pronunciation or dictionary
sources.

`Current result` records the exact output of `romanize(input)` at master commit
`bf24151556a5e4bf3e4643f65067b63d9dce9cbb`. `NIKL RR` and `Current result`
display the exact strings, including capitalization, spaces, punctuation,
hyphens, and parenthesized variants. For the core comparison in Section 2 and
Section 3(1), `passing` ignores initial capitalization only. No other
normalization is used.

Inventory equality does not automatically establish a public formatting
guarantee. In particular, equality in an `outside core contract` row is
incidental and is not a guarantee that the default API supports that
provision's formatting.

## Interpretation

The categories are:

- `passing`: the current result matches the core comparison defined above.
- `locally derivable`: a mismatch is covered by a general official rule whose
  application can be determined from local phonological context.
- `morphology/lexicon-dependent`: correct application requires morphology,
  segmentation, lexical class, or conventional lexical knowledge.
- `special transcription`: the example belongs to an optional, formatting,
  naming, administrative, or reversible spelling-based transcription
  provision outside default pronunciation-based romanization.

The dispositions are:

- `protected test`: the intended disposition is regression protection. A
  specific test-case reference in `Related test or issue` means the entry is
  already protected; `candidate: tests/test_rr_correctness.py` means the entry
  is eligible for a later source-backed fixture and does not claim that such a
  test currently exists.
- `one-rule-family candidate`: the entry identifies the single bounded general
  rule family eligible for a later behavior-changing change.
- `documented limitation`: the entry is recorded without making it an
  implementation target.
- `outside core contract`: the special provision is not promised by the
  default pronunciation-based API.

`none (inventory only)` means there is no related test or issue and no
implementation commitment. Morphology/lexicon-dependent and special-
transcription entries are documented boundaries and do not block v1.0.0.

## Section 2 consonant Note 1

| Input | Shown pronunciation | NIKL RR | Current result | Category | Disposition | Related test or issue |
| --- | --- | --- | --- | --- | --- | --- |
| 구미 | — | Gumi | gumi | passing | protected test | tests/test_characterization.py::test_preserves_non_hangul_boundaries_current_behavior |
| 영동 | — | Yeongdong | yeongdong | passing | protected test | tests/test_characterization.py::test_preserves_non_hangul_boundaries_current_behavior |
| 백암 | — | Baegam | baegam | passing | protected test | candidate: tests/test_rr_correctness.py |
| 옥천 | — | Okcheon | okcheon | passing | protected test | candidate: tests/test_rr_correctness.py |
| 합덕 | — | Hapdeok | hapdeok | passing | protected test | candidate: tests/test_rr_correctness.py |
| 호법 | — | Hobeop | hobeop | passing | protected test | candidate: tests/test_rr_correctness.py |
| 월곶 | 월곧 | Wolgot | wolgot | passing | protected test | candidate: tests/test_rr_correctness.py |
| 벚꽃 | 벋꼳 | beotkkot | beotkkot | passing | protected test | candidate: tests/test_rr_correctness.py |
| 한밭 | 한받 | Hanbat | hanbat | passing | protected test | candidate: tests/test_rr_correctness.py |

## Section 2 liquid Note 2

| Input | Shown pronunciation | NIKL RR | Current result | Category | Disposition | Related test or issue |
| --- | --- | --- | --- | --- | --- | --- |
| 구리 | — | Guri | guri | passing | protected test | candidate: tests/test_rr_correctness.py |
| 설악 | — | Seorak | seorak | passing | protected test | candidate: tests/test_rr_correctness.py |
| 칠곡 | — | Chilgok | chilgok | passing | protected test | candidate: tests/test_rr_correctness.py |
| 임실 | — | Imsil | imsil | passing | protected test | candidate: tests/test_rr_correctness.py |
| 울릉 | — | Ulleung | ulleung | passing | protected test | tests/test_rr_correctness.py::test_liquid_and_nasal_assimilation_rr_correctness[울릉-ulleung] |
| 대관령 | 대괄령 | Daegwallyeong | daegwallyeong | passing | protected test | tests/test_rr_correctness.py::test_liquid_and_nasal_assimilation_rr_correctness[대관령-daegwallyeong] |

## Section 3(1) adjacent-consonant assimilation

| Input | Shown pronunciation | NIKL RR | Current result | Category | Disposition | Related test or issue |
| --- | --- | --- | --- | --- | --- | --- |
| 백마 | 뱅마 | Baengma | baekma | locally derivable | one-rule-family candidate | candidate: tests/test_rr_correctness.py |
| 신문로 | 신문노 | Sinmunno | sinmunno | passing | protected test | tests/test_rr_correctness.py::test_n_r_to_n_exception_rr_correctness[신문로-sinmunno] |
| 종로 | 종노 | Jongno | jongno | passing | protected test | tests/test_rr_correctness.py::test_liquid_and_nasal_assimilation_rr_correctness[종로-jongno] |
| 왕십리 | 왕심니 | Wangsimni | wangsimni | passing | protected test | tests/test_rr_correctness.py::test_rieul_to_n_after_nasal_and_stop_codas_rr_correctness[왕십리-wangsimni] |
| 별내 | 별래 | Byeollae | byeollae | passing | protected test | tests/test_rr_correctness.py::test_liquid_and_nasal_assimilation_rr_correctness[별내-byeollae] |
| 신라 | 실라 | Silla | silla | passing | protected test | tests/test_rr_correctness.py::test_liquid_and_nasal_assimilation_rr_correctness[신라-silla] |

## Section 3(1) epenthetic ㄴ and ㄹ

| Input | Shown pronunciation | NIKL RR | Current result | Category | Disposition | Related test or issue |
| --- | --- | --- | --- | --- | --- | --- |
| 학여울 | 항녀울 | Hangnyeoul | hagyeoul | morphology/lexicon-dependent | documented limitation | none (inventory only) |
| 알약 | 알략 | allyak | aryak | morphology/lexicon-dependent | documented limitation | none (inventory only) |

## Section 3(1) palatalization

| Input | Shown pronunciation | NIKL RR | Current result | Category | Disposition | Related test or issue |
| --- | --- | --- | --- | --- | --- | --- |
| 해돋이 | 해도지 | haedoji | haedoji | passing | protected test | tests/test_rr_correctness.py::test_palatalization_rr_correctness[해돋이-haedoji] |
| 같이 | 가치 | gachi | gachi | passing | protected test | tests/test_rr_correctness.py::test_palatalization_rr_correctness[같이-gachi] |
| 굳히다 | 구치다 | guchida | guchida | passing | protected test | tests/test_rr_correctness.py::test_palatalization_rr_correctness[굳히다-guchida] |

## Section 3(1) consonants adjacent to ㅎ

| Input | Shown pronunciation | NIKL RR | Current result | Category | Disposition | Related test or issue |
| --- | --- | --- | --- | --- | --- | --- |
| 좋고 | 조코 | joko | joko | passing | protected test | tests/test_rr_correctness.py::test_h_adjacency_rr_correctness[좋고-joko] |
| 놓다 | 노타 | nota | nota | passing | protected test | tests/test_rr_correctness.py::test_h_adjacency_rr_correctness[놓다-nota] |
| 잡혀 | 자펴 | japyeo | japyeo | passing | protected test | tests/test_rr_correctness.py::test_h_adjacency_rr_correctness[잡혀-japyeo] |
| 낳지 | 나치 | nachi | nachi | passing | protected test | tests/test_rr_correctness.py::test_h_adjacency_rr_correctness[낳지-nachi] |

## Section 3(1) noun exception after ㅎ

| Input | Shown pronunciation | NIKL RR | Current result | Category | Disposition | Related test or issue |
| --- | --- | --- | --- | --- | --- | --- |
| 묵호 | — | Mukho | mukho | passing | protected test | tests/test_rr_correctness.py::test_h_adjacency_noun_examples_do_not_transcribe_aspiration[묵호-mukho] |
| 집현전 | — | Jiphyeonjeon | jiphyeonjeon | passing | protected test | tests/test_rr_correctness.py::test_h_adjacency_noun_examples_do_not_transcribe_aspiration[집현전-jiphyeonjeon] |

## Section 3(1) compound-morpheme tensification note

| Input | Shown pronunciation | NIKL RR | Current result | Category | Disposition | Related test or issue |
| --- | --- | --- | --- | --- | --- | --- |
| 압구정 | — | Apgujeong | apgujeong | passing | protected test | candidate: tests/test_rr_correctness.py |
| 낙동강 | — | Nakdonggang | nakdonggang | passing | protected test | candidate: tests/test_rr_correctness.py |
| 죽변 | — | Jukbyeon | jukbyeon | passing | protected test | candidate: tests/test_rr_correctness.py |
| 낙성대 | — | Nakseongdae | nakseongdae | passing | protected test | candidate: tests/test_rr_correctness.py |
| 합정 | — | Hapjeong | hapjeong | passing | protected test | candidate: tests/test_rr_correctness.py |
| 팔당 | — | Paldang | paldang | passing | protected test | candidate: tests/test_rr_correctness.py |
| 샛별 | — | saetbyeol | saetbyeol | passing | protected test | candidate: tests/test_rr_correctness.py |
| 울산 | — | Ulsan | ulsan | passing | protected test | candidate: tests/test_rr_correctness.py |

## Section 3(2) optional pronunciation-disambiguating hyphen

| Input | Shown pronunciation | NIKL RR | Current result | Category | Disposition | Related test or issue |
| --- | --- | --- | --- | --- | --- | --- |
| 중앙 | — | Jung-ang | jungang | special transcription | outside core contract | none (inventory only) |
| 반구대 | — | Ban-gudae | bangudae | special transcription | outside core contract | none (inventory only) |
| 세운 | — | Se-un | seun | special transcription | outside core contract | none (inventory only) |
| 해운대 | — | Hae-undae | haeundae | special transcription | outside core contract | none (inventory only) |

## Section 3(3) proper-name capitalization

| Input | Shown pronunciation | NIKL RR | Current result | Category | Disposition | Related test or issue |
| --- | --- | --- | --- | --- | --- | --- |
| 부산 | — | Busan | busan | special transcription | outside core contract | none (inventory only) |
| 세종 | — | Sejong | sejong | special transcription | outside core contract | none (inventory only) |

## Section 3(4) personal-name formatting

| Input | Shown pronunciation | NIKL RR | Current result | Category | Disposition | Related test or issue |
| --- | --- | --- | --- | --- | --- | --- |
| 민용하 | — | Min Yongha (Min Yong-ha) | minyongha | special transcription | outside core contract | none (inventory only) |
| 송나리 | — | Song Nari (Song Na-ri) | songnari | special transcription | outside core contract | none (inventory only) |

## Section 3(4) given-name assimilation exception

| Input | Shown pronunciation | NIKL RR | Current result | Category | Disposition | Related test or issue |
| --- | --- | --- | --- | --- | --- | --- |
| 한복남 | — | Han Boknam (Han Bok-nam) | hanboknam | special transcription | outside core contract | none (inventory only) |
| 홍빛나 | — | Hong Bitna (Hong Bit-na) | hongbitna | special transcription | outside core contract | none (inventory only) |

## Section 3(5) administrative units

| Input | Shown pronunciation | NIKL RR | Current result | Category | Disposition | Related test or issue |
| --- | --- | --- | --- | --- | --- | --- |
| 충청북도 | — | Chungcheongbuk-do | chungcheongbukdo | special transcription | outside core contract | none (inventory only) |
| 제주도 | — | Jeju-do | jejudo | special transcription | outside core contract | none (inventory only) |
| 의정부시 | — | Uijeongbu-si | uijeongbusi | special transcription | outside core contract | none (inventory only) |
| 양주군 | — | Yangju-gun | yangjugun | special transcription | outside core contract | none (inventory only) |
| 도봉구 | — | Dobong-gu | dobonggu | special transcription | outside core contract | none (inventory only) |
| 신창읍 | — | Sinchang-eup | sinchangeup | special transcription | outside core contract | none (inventory only) |
| 삼죽면 | — | Samjuk-myeon | samjukmyeon | special transcription | outside core contract | none (inventory only) |
| 인왕리 | — | Inwang-ri | inwangri | special transcription | outside core contract | tests/test_rr_correctness.py::test_administrative_unit_ri_preserves_rr_spelling |
| 당산동 | — | Dangsan-dong | dangsandong | special transcription | outside core contract | none (inventory only) |
| 봉천1동 | — | Bongcheon 1(il) -dong | bongcheon1dong | special transcription | outside core contract | none (inventory only) |
| 종로 2가 | — | Jongno 2(i) -ga | jongno 2ga | special transcription | outside core contract | none (inventory only) |
| 퇴계로 3가 | — | Toegyero 3(sam) -ga | toegyero 3ga | special transcription | outside core contract | none (inventory only) |

## Section 3(6) geographic features, cultural properties, and structures

| Input | Shown pronunciation | NIKL RR | Current result | Category | Disposition | Related test or issue |
| --- | --- | --- | --- | --- | --- | --- |
| 남산 | — | Namsan | namsan | special transcription | outside core contract | none (inventory only) |
| 속리산 | — | Songnisan | songnisan | special transcription | outside core contract | none (inventory only) |
| 금강 | — | Geumgang | geumgang | special transcription | outside core contract | none (inventory only) |
| 독도 | — | Dokdo | dokdo | special transcription | outside core contract | none (inventory only) |
| 경복궁 | — | Gyeongbokgung | gyeongbokgung | special transcription | outside core contract | none (inventory only) |
| 무량수전 | — | Muryangsujeon | muryangsujeon | special transcription | outside core contract | none (inventory only) |
| 연화교 | — | Yeonhwagyo | yeonhwagyo | special transcription | outside core contract | none (inventory only) |
| 극락전 | — | Geungnakjeon | geungnakjeon | special transcription | outside core contract | none (inventory only) |
| 안압지 | — | Anapji | anapji | special transcription | outside core contract | none (inventory only) |
| 남한산성 | — | Namhansanseong | namhansanseong | special transcription | outside core contract | none (inventory only) |
| 화랑대 | — | Hwarangdae | hwarangdae | special transcription | outside core contract | none (inventory only) |
| 불국사 | — | Bulguksa | bulguksa | special transcription | outside core contract | none (inventory only) |
| 현충사 | — | Hyeonchungsa | hyeonchungsa | special transcription | outside core contract | none (inventory only) |
| 독립문 | — | Dongnimmun | dongnipmun | special transcription | outside core contract | none (inventory only) |
| 오죽헌 | — | Ojukheon | ojukheon | special transcription | outside core contract | none (inventory only) |
| 촉석루 | — | Chokseongnu | chokseongnu | special transcription | outside core contract | none (inventory only) |
| 종묘 | — | Jongmyo | jongmyo | special transcription | outside core contract | none (inventory only) |
| 다보탑 | — | Dabotap | dabotap | special transcription | outside core contract | none (inventory only) |

## Section 3(8) reversible spelling-based transcription

| Input | Shown pronunciation | NIKL RR | Current result | Category | Disposition | Related test or issue |
| --- | --- | --- | --- | --- | --- | --- |
| 집 | — | jib | jip | special transcription | outside core contract | none (inventory only) |
| 짚 | — | jip | jip | special transcription | outside core contract | none (inventory only) |
| 밖 | — | bakk | bak | special transcription | outside core contract | none (inventory only) |
| 값 | — | gabs | gap | special transcription | outside core contract | none (inventory only) |
| 붓꽃 | — | buskkoch | butkkot | special transcription | outside core contract | none (inventory only) |
| 먹는 | — | meogneun | meokneun | special transcription | outside core contract | none (inventory only) |
| 독립 | — | doglib | dongnip | special transcription | outside core contract | none (inventory only) |
| 문리 | — | munli | mulli | special transcription | outside core contract | none (inventory only) |
| 물엿 | — | mul-yeos | muryeot | special transcription | outside core contract | none (inventory only) |
| 굳이 | — | gud-i | guji | special transcription | outside core contract | tests/test_rr_correctness.py::test_palatalization_rr_correctness[굳이-guji] |
| 좋다 | — | johda | jota | special transcription | outside core contract | none (inventory only) |
| 가곡 | — | gagog | gagok | special transcription | outside core contract | none (inventory only) |
| 조랑말 | — | jolangmal | jorangmal | special transcription | outside core contract | none (inventory only) |
| 없었습니다. | — | eobs-eoss-seubnida | eopseotseupnida. | special transcription | outside core contract | none (inventory only) |

## Summary

The inventory contains 94 entries in 15 official groups.

Category counts:

- 37 `passing`
- 1 `locally derivable`
- 2 `morphology/lexicon-dependent`
- 54 `special transcription`

Disposition counts:

- 37 `protected test`
- 1 `one-rule-family candidate`
- 2 `documented limitation`
- 54 `outside core contract`

The next behavior-change candidate is only the general nasal-assimilation
family represented by 백마[뱅마]. The documented morphology/lexicon limitations
are 학여울 and 알약; they are not implementation targets.

The seven special-transcription groups outside the core contract are Section
3(2) optional pronunciation-disambiguating hyphen, Section 3(3) proper-name
capitalization, Section 3(4) personal-name formatting, Section 3(4) given-name
assimilation exception, Section 3(5) administrative units, Section 3(6)
geographic features, cultural properties, and structures, and Section 3(8)
reversible spelling-based transcription.
