# Modernization Plan

This plan is current through PR #58 on 2026-07-24 and includes the Stage 3
inventory in this change. It replaces the earlier open-ended PR checklist
with finite work stages leading to v1.0.0.

The project will maintain a **bounded deterministic core**: every Python
`str` input must produce a `str` without leaking an internal exception, while
strict correctness claims remain limited to source-backed rules that the
existing pipeline can derive reliably. Morphology-dependent pronunciation,
lexical exceptions, proper-name conventions, and special transcription
formatting are documented honestly rather than guessed.

## Current State

### Architecture

The package is a small, dependency-free Python library and CLI:

1. `korean_romanizer.romanizer.romanize(text)` is the preferred public flow.
   It sends the input through pronunciation normalization and then romanizes
   the pronounced characters.
2. `korean_romanizer.pronouncer.Pronouncer` creates mutable `Syllable`
   objects, applies ordered context-sensitive substitutions, and exposes the
   resulting string through `pronounced`.
3. `korean_romanizer.syllable.Syllable` decomposes and reconstructs
   precomposed Hangul through Unicode arithmetic.
4. `korean_romanizer.romanizer.Romanizer` remains a compatibility wrapper:
   `Romanizer(text).romanize()` delegates to `romanize(text)`.
5. `korean_romanizer.cli` provides the `kroman` console script.

The project uses a flat package layout. Romanization tables and pronunciation
rules remain Python module data rather than external datasets.

### Tests and Quality Gates

The current suite collects 244 tests:

- `tests/test_characterization.py` preserves mixed text, whitespace,
  compatibility jamo, and existing pronunciation behavior.
- `tests/test_syllable_characterization.py` records reconstruction semantics:
  `Syllable.__repr__` is non-mutating, while `__str__` and
  `construct_syllable()` retain their existing mutation behavior.
- `tests/test_unicode_characterization.py` records current NFC, NFD, modern
  decomposed-jamo, compatibility-jamo, and archaic-jamo behavior.
- `tests/test_rr_correctness.py` contains source-backed Revised Romanization
  fixtures.
- `tests/test_totality.py` covers the final-`ㅎ` coda family at non-syllable
  boundaries and checks all 28 precomposed coda states against every open
  Hangul onset/medial shape plus representative boundary classes.
- `tests/test_public_api.py`, `tests/test_cli.py`, and
  `tests/test_benchmarks.py` protect imports, the console contract, and the
  dependency-free benchmark harness.

CI tests Python 3.10, 3.11, 3.12, and 3.13. Quality gates run pytest, Ruff,
mypy, package builds, and `scripts/validate_wheel_metadata.py`. The wheel
validator installs the built wheel in an isolated environment, validates
metadata and package contents, imports the public API, and runs `kroman`.

### Packaging and Release Setup

- `pyproject.toml` contains PEP 621 project metadata.
- `requires-python` is `>=3.10`; classifiers match the current CI matrix.
- Versions are derived from Git tags through `setuptools_scm`.
- The `dev` extra includes test, lint, type-check, coverage, and build tools.
- GitHub releases trigger the PyPI publishing workflow.
- `CHANGELOG.md` now has an Unreleased section, initially covering PR #57.

The publishing workflow still uses a PyPI token, builds within the publishing
job, and uses older checkout/setup-python major versions. Those are bounded
Stage 5 tasks, not reasons to reopen completed core refactors.

## Stable Public Surface

The preferred supported surface is:

- `from korean_romanizer import romanize`
- `romanize(text) -> str` for `str` input
- the `kroman` console script

Compatibility surfaces remain supported until an explicit deprecation:

- `Romanizer(text).romanize()`
- `Pronouncer`
- `Syllable`
- the four names exported by `korean_romanizer.__all__`

Mixed non-Korean text, punctuation, and whitespace remain preserved by the
library unless a focused change is documented and tested. The CLI's
argument-joining behavior is separately subject to the Stage 4 contract
decision.

Module-level tables, constants, and private helpers remain implementation
details even when Python makes them importable. Stage 4 will define the
supported lower-level behavior narrowly; it will not convert every historical
internal import into a permanent public API.

## Bounded Correctness Policy

Correctness work is divided into four categories:

1. **Safety invariants.** Every Python `str` input must complete and return a
   `str`, including mixed text and unsupported Unicode characters.
2. **Locally derivable rules.** The deterministic pipeline may implement a
   rule when it has enough observable context and an official source supports
   the expected output.
3. **Morphology- or lexicon-dependent cases.** Cases that require morpheme
   boundaries, word segmentation, lexical class, or a conventional spelling
   are classified and documented unless a narrow source-backed exception is
   already protected.
4. **Special transcription provisions.** Proper-name capitalization,
   administrative-unit hyphenation, personal-name formatting, and accepted
   conventional spellings remain outside the default core transliterator.

Only passing examples, deliberately implemented locally derivable rules, and
explicitly inventoried narrow exceptions with source-backed regressions belong
in the strict RR-correctness suite. Generated combinations may prove a safety
property such as completion or return type; they must not be presented as
evidence that invented syllable pairs are linguistically correct.

The public data flow remains:

1. `romanize(text)` invokes `Pronouncer`.
2. `Pronouncer` applies ordered substitutions.
3. The pronounced result is converted through the onset, vowel, and coda
   tables.
4. Unsupported or non-Korean characters are preserved and reset adjacent
   Hangul context.

The strengthened internal invariant is that pronunciation must not hand the
romanization stage a Hangul coda absent from the strict coda table. PR #57
repaired the known final-`ㅎ` leak and added direct and public-API safety
coverage. Future rule changes must preserve that invariant rather than hide
missed substitutions behind a permissive table lookup.

## Known Limits and Change Gates

Known pre-v1.0 contract work:

- The algorithm has no morphology or word-segmentation model. Epenthetic
  `ㄴ`/`ㄹ`, some assimilation boundaries, and lexical exceptions cannot
  always be inferred from adjacent code points.
- Modern decomposed jamo are preserved inconsistently with precomposed Hangul;
  automatic normalization remains an explicit Stage 4 decision.
- Non-string input currently follows natural implementation exceptions rather
  than a documented contract.
- `kroman` has no stdin mode and joins positional arguments with spaces.
- `Syllable.__repr__` is now non-mutating, but `__str__` and
  `construct_syllable()` still mutate `char`; Stage 4 must preserve or
  explicitly change and test that compatibility behavior.
- `Pronouncer` mutates adjacent syllables in rule order. New helper behavior
  needs focused regression and order-sensitive coverage.
- Proper names and administrative units cannot be handled reliably through
  hidden guesses in the core transliterator.

The following work is outside the critical path to v1.0.0:

- A morphological analyzer, general lexicon, caller override API, or
  proper-name database requires a separate post-v1.0.0 design.
- Performance optimization requires a measured problem and same-environment
  before/after benchmark evidence.
- Broad Unicode expansion or broad refactoring requires its own design and
  must not be bundled with a rule or release change.

## Completed Modernization

The foundation completed before PR #58 includes:

- development bootstrap, supported-Python CI, characterization tests, and
  packaging-metadata cleanup (PRs #31-#35);
- table organization and source-backed liquid/nasal, palatalization, and
  `ㅎ`-adjacency fixes (PRs #36, #37, #39, and #40);
- the preferred functional API, explicit exports, PEP 621 metadata,
  SCM-derived versions, and installed-wheel validation (PRs #42-#43);
- extraction of all pronunciation rule blocks into focused private helpers
  (PRs #46-#48 and #52-#53);
- Unicode characterization, `kroman --version`, and the dependency-free
  benchmark baseline (PRs #49-#51);
- the prior roadmap refresh after PR #53 (PR #54).

Recent work closed the previous next step and the first bounded safety stage:

- PR #55 characterized `Syllable` representation and reconstruction side
  effects.
- PR #56 made `Syllable.__repr__` non-mutating while retaining the existing
  `__str__` and `construct_syllable()` behavior.
- PR #57 reduced leftover final-`ㅎ` family codas before romanization, added
  source-backed `많고` and `꿇리다` fixtures, added the exhaustive local
  coda/follower safety matrix, and created the initial changelog.

- PR #58 refreshed the bounded roadmap, adopted the bounded correctness
  categories, finite stages, and exit criteria, and named the RR inventory as
  Stage 3.

## Work Stages

### Stage 1: Refresh the Roadmap

**Status:** Complete in PR #58.

Completed scope:

- Update the repository snapshot through PR #57.
- Record PRs #55-#57 and remove the completed `Syllable.__repr__` task.
- Replace open-ended PR headings with finite stages and exit criteria.
- Adopt the bounded correctness categories and v1.0.0 boundary.
- Name the Stage 3 RR inventory and its source scope as the then-next
  artifact.
- Record release-note debt for observable changes since v0.28.0, including
  PR #56.

**Exit criterion:** PR #58 accurately described `master` through PR #57,
named Stage 3 and its source scope as next, contained no completed task under
remaining work, and met this criterion.

### Stage 2: Restore String Totality

**Status:** Complete in PR #57.

Completed scope:

- Add boundary regressions for `않 `, `많!`, and `싫?`.
- Add source-backed Hangul-boundary guards for `많고[만코]` and
  `꿇리다[꿀리다]`.
- Repair final-`ㅎ` family handling at the pronunciation boundary without
  weakening the coda table.
- Check all 28 precomposed coda states against all 399 open Hangul
  onset/medial followers and 12 representative non-syllable boundary classes.
- Preserve exact-output claims for source-backed or explicitly documented
  library-boundary fixtures only.

**Exit criterion:** Focused regressions pass, the local coda/boundary matrix
finds no internal exception or non-string result, and the existing suite
remains green. PR #57 met this criterion.

### Stage 3: Build a Bounded RR Inventory

**Status:** Complete in this inventory refresh.

Completed scope: `docs/rr-inventory.md` inventories every word- and name-level
example on the
National Institute of Korean Language's English
[Romanization of Korean](https://www.korean.go.kr/front_eng/roman/roman_01.do)
page as captured on 2026-07-23, including the examples in the Section 2 notes
and all Section 3 provisions. The base jamo mapping rows are covered by the
existing table tests and are not separate inventory entries. Supporting NIKL
pronunciation rules or dictionary entries may justify a classification but do
not expand the primary inventory scope.

Each inventory entry records:

- source section and example;
- input text and shown pronunciation, when provided;
- expected Revised Romanization form;
- current library result;
- category: passing, locally derivable, morphology/lexicon-dependent, or
  special transcription;
- disposition: protected test, one-rule-family candidate, documented
  limitation, or outside the core contract;
- related test or issue reference.

`docs/rr-inventory.md` contains exactly 94 examples in 15 groups, measured at
`bf24151`: 37 passing, 1 locally derivable, 2 morphology/lexicon-dependent,
and 54 special transcription. Its dispositions are 38 `protected test`, 1
`one-rule-family candidate`, 2 `documented limitation`, and 53 `outside core
contract`.

The only next behavior-change candidate is general nasal assimilation,
represented by 백마[뱅마]. 학여울 and 알약 are documented limitations. Any
behavior implementation must be a separate source-backed one-rule-family
change. No runtime behavior or tests changed in this inventory refresh.

**Exit criterion:** Met. Every example in the dated primary source snapshot
has a source, category, current result, and explicit disposition. Strict
correctness tests contain only passing cases, deliberately implemented locally
derivable rules, or explicitly protected narrow exceptions. Unimplemented
morphology-dependent and special-provision cases are documented and do not
block release.

### Stage 4: Finish Contract Decisions

**Status:** Next.

Decide and document:

- whether Unicode normalization and modern decomposed-jamo handling are
  automatic, optional, or intentionally unchanged;
- whether `kroman` accepts stdin and how positional whitespace is handled;
- whether non-string input has an explicit `TypeError` contract or preserves
  current natural exceptions;
- the supported lower-level compatibility surface, including `Pronouncer`,
  `Syllable`, `Syllable.__str__`, and `construct_syllable()`, while keeping
  module tables and private helpers outside the stable contract.

**Exit criterion:** Each decision is documented as either implemented and
tested or intentionally preserving current behavior. No unresolved contract
question remains on the v1.0.0 checklist.

### Stage 5: Harden Tooling and Publishing

**Status:** Pending.

Required scope:

- Add Python 3.14 to CI and package classifiers.
- Refresh test and publishing workflows to current maintained action majors.
- Build wheel and sdist once, validate those exact artifacts, upload them, and
  pass the same artifacts to a separate publishing job.
- Move PyPI publishing to trusted publishing with narrowly scoped
  `id-token: write`.
- Verify tagged and untagged `setuptools_scm` versions.
- Make installed-console-script testing hermetic instead of discovering an
  unrelated ambient installation.
- Backfill `CHANGELOG.md` for observable changes since v0.28.0, including the
  PR #56 representation change, and add a release checklist.
- Validate the production-equivalent flow through TestPyPI or an isolated dry
  run.

**Exit criterion:** The supported Python matrix passes; one validated artifact
set flows unchanged through the release jobs; trusted publishing, SCM
versions, changelog, release checklist, and installed CLI have been exercised
in the production-equivalent path.

### Stage 6: Stabilize and Release

**Status:** Future.

Required scope:

- Publish v0.29.0 as the pre-1.0 stabilization release.
- Before publishing v0.29.0, record a calendar cutoff for collecting
  release-blocking regressions; snapshot the finite blocker list at that
  cutoff.
- Resolve each blocker or explicitly defer it with a documented limitation.
- Freeze the v1.0.0 public API, supported-Python versions, and documented
  behavior guarantees.
- Ensure every known correctness gap is fixed, documented, or explicitly
  outside the core contract.
- Publish v1.0.0 only from the exact artifacts produced by the hardened
  release flow.

**Exit criterion:** v0.29.0 has completed its dated stabilization window; the
finite blocker list is resolved or explicitly deferred; API, Python, behavior,
changelog, and known-limit guarantees have been reviewed; and v1.0.0 is
published through the validated workflow.

## Testing and Release Policy

- Use regression-first development for every bug or correctness change.
- Keep characterization fixtures separate from source-backed RR correctness
  fixtures.
- Use exhaustive or generated tests for safety properties only, not invented
  linguistic expectations.
- Add direct helper or rule-order tests immediately before changing the
  relevant `Pronouncer` helper.
- Run pytest, configured Ruff checks, mypy, package build, and wheel metadata
  validation for implementation changes.
- Record same-environment before/after numbers for performance changes.
- Any observable change to `romanize`, `Romanizer`, `kroman`, `Pronouncer`, or
  `Syllable` requires focused regression tests and an Unreleased changelog
  entry. Correctness changes must identify their official source.
- Release v0.29.0 before v1.0.0 so accumulated modernization changes receive
  production exposure before the stable contract is frozen.
