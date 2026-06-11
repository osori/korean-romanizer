# Modernization Plan

This plan covers the `korean-romanizer` Python package in this repository. It is
based on the current source tree, tests, packaging metadata, and GitHub Actions
workflows.

## Current Architecture

The project is a small, dependency-free Python package that romanizes Hangul
text using a rule-based pipeline:

1. `korean_romanizer.syllable.Syllable` decomposes a single precomposed Hangul
   syllable into initial, medial, and final jamo using Unicode arithmetic. It can
   also reconstruct the syllable after those pieces are mutated.
2. `korean_romanizer.pronouncer.Pronouncer` builds a list of `Syllable` objects
   for the input text and applies context-sensitive pronunciation substitutions.
   It mutates adjacent `Syllable` instances in place, then exposes the resulting
   string through `pronounced`.
3. `korean_romanizer.romanizer.Romanizer` passes text through `Pronouncer`, walks
   the pronounced string character by character, decomposes Hangul syllables
   again, and maps jamo to Latin strings through module-level dictionaries.
4. `korean_romanizer.cli` is a thin `argparse` wrapper. It joins positional
   arguments with spaces, romanizes that string, and prints the result.

The package uses a flat source layout, not a `src/` layout. The core tables and
rules live in module globals rather than structured data files. There are no
runtime dependencies.

## Public API Surface

The package currently exposes more than the documented API:

- `from korean_romanizer.romanizer import Romanizer` is the README-documented
  library API. `Romanizer(text).romanize()` returns a romanized string.
- `from korean_romanizer import Romanizer, Pronouncer, Syllable` works because
  `korean_romanizer/__init__.py` re-exports all three classes.
- `korean_romanizer.syllable.Syllable` exposes mutable attributes
  `char`, `initial`, `medial`, and `final`, plus methods
  `separate_syllable`, `construct_syllable`, `is_hangul`, and
  `final_to_initial`.
- `korean_romanizer.pronouncer.Pronouncer` exposes `pronounced` and
  `final_substitute`.
- Module-level constants and dictionaries are importable, including
  `vowel`, `onset`, `coda`, `compat_onset`, `unicode_initial`,
  `unicode_medial`, `unicode_final`, `unicode_compatible_consonants`,
  `unicode_compatible_finals`, `double_consonant_final`, and
  `NULL_CONSONANT`.
- The package installs the `kroman` console script, mapped to
  `korean_romanizer.cli:main`.
- `python -m korean_romanizer.cli ...` also works.

There is no explicit compatibility policy, `__all__`, type information, or
deprecation path. Any modernization should first decide which of these imports
are stable public API and which are internal implementation details.

## Existing Tests and Gaps

Current tests:

- `tests/test_romanizer.py` contains example-based tests for common words,
  spacing, onset/coda mappings, final-consonant substitutions, double-final
  behavior, non-syllable jamo, and some `ㅎ` cases.
- `tests/test_cli.py` checks that `python -m korean_romanizer.cli` matches the
  library for several inputs, prints help, errors on missing arguments, handles a
  long argument list, and smoke-tests the installed `kroman` console script when
  available.
- CI installs the package with `pip install .`, runs a limited `flake8` check,
  then runs `pytest` on Python 3.10.
- Local baseline: after bootstrapping temporary test dependencies under `/tmp`,
  `python3 -m pytest -q` on Python 3.12.3 reports `19 passed, 1 skipped`.

Observed test gaps:

- The local environment initially had Python 3.12, but no `pytest`, `pip`, or
  `python3.12-venv`, so there is no straightforward project-owned local test
  bootstrap path.
- Tests focus on `Romanizer`; `Syllable` and `Pronouncer` internals have no
  direct unit tests despite carrying most rule complexity.
- There is no golden corpus from the official Revised Romanization rules or from
  known dictionary examples.
- Several important phonological cases are missing or commented out, including
  liquid/nasal assimilation examples such as `울릉` and `대관령`.
- There is little coverage for Unicode normalization forms, decomposed jamo,
  archaic jamo, punctuation, mixed whitespace preservation, invalid input types,
  and very large text.
- The CLI tests intentionally join arguments with spaces, but do not define
  whether preserving original whitespace is part of the contract.
- There is no coverage reporting, no Python version matrix, no build artifact
  check in CI, and no test for generated package metadata.

## Packaging and Release Setup

Current packaging:

- `pyproject.toml` declares a PEP 517 build using `setuptools.build_meta` with
  `setuptools>=42` and `setuptools_scm[toml]>=6.2`.
- `setup.py` contains package metadata, manually lists `packages =
  ['korean_romanizer']`, enables `use_scm_version=True`, and registers the
  `kroman` console script.
- `setup.cfg` contains legacy metadata (`description-file = README.md`) and an
  empty `[tool.setuptools_scm]` section.
- The package name is `korean_romanizer`; the repository and README title use
  `korean-romanizer`.

Release setup:

- `.github/workflows/python-app.yml` runs CI on pushes and pull requests against
  `master` with Python 3.10.
- `.github/workflows/python-publish.yml` builds with `python -m build` and
  publishes to PyPI using `pypa/gh-action-pypi-publish` when a GitHub release is
  published.
- Versions come from Git tags through `setuptools_scm`.

Packaging and release gaps:

- README release instructions say publishing is triggered by either a version tag
  or GitHub release, but the workflow only listens for `release: published`.
- Metadata still lives mostly in `setup.py`; modern projects usually put this in
  `[project]` in `pyproject.toml`.
- There is no `requires-python`. Classifiers list Python 3.4, 3.5, and 3.6 even
  though CI uses Python 3.10 and modern build tooling may not support those old
  versions.
- There is no documented development extra such as `.[dev]`, and no local
  bootstrap path for tests.
- There is no `long_description`/`readme` metadata in the modern project table,
  no typed-package marker, and no project URLs beyond the homepage in
  `setup.py`.
- The publish workflow uses a PyPI API token secret rather than PyPI trusted
  publishing via OpenID Connect.
- GitHub Actions use older major versions of `actions/checkout` and
  `actions/setup-python`.

## Likely Correctness Risks

- The implementation does not cover all Revised Romanization edge cases. Direct
  checks show outputs such as `같이 -> gati`, `종로 -> jongro`,
  `신라 -> sinra`, `울릉 -> ulreung`, and `대관령 -> daegwanryeong`; several of
  these are known assimilation or palatalization cases that likely need explicit
  rules.
- Decomposed modern jamo are not consistently romanized. For example, `ᄀ` is
  currently preserved because the romanizer's Hangul regex covers precomposed
  Hangul and compatibility jamo, but not the modern choseong/jongseong Unicode
  blocks.
- The algorithm has no morphology or word-boundary model. Some Korean
  romanization rules depend on morpheme boundaries, proper nouns, names, or
  conventional spellings, which a pure character-neighborhood pass cannot infer.
- `Pronouncer.final_substitute` mutates adjacent syllables in place and depends
  on rule order. Adding rules without characterization tests could silently
  change earlier behavior.
- `Syllable.__repr__` reconstructs and mutates `self.char`, which is surprising
  for a representation method and could make debugging or future caching
  behavior confusing.
- Some mappings appear inconsistent or dead, such as `double_consonant_final`
  containing compatibility `ㅆ` while full-syllable finals use `ᆻ`.
- `Romanizer` assumes pronunciation normalization has reduced all finals to the
  seven codas represented in `coda`. Missed substitutions can become `KeyError`
  failures instead of graceful fallback behavior.
- Public imports are broader than the documented API, so internal refactors could
  break users who import `Pronouncer`, `Syllable`, or module-level tables.

## Performance Risks

- Romanization is linear in input size conceptually, but it does two character
  passes and creates `Syllable` objects in both `Pronouncer` and `Romanizer`.
- `Romanizer.romanize()` builds the output with repeated string concatenation.
  For large inputs this can degrade compared with appending to a list and
  joining once.
- The Hangul check calls `re.match` for every character with a string pattern.
  The regex cache helps, but a precompiled regex or direct Unicode range checks
  would reduce overhead.
- `Pronouncer` reconstructs a full pronounced string before romanization. A
  future streaming or single-pass design could avoid intermediate strings, but
  should come after correctness characterization.
- There are no benchmarks, so performance changes cannot currently be evaluated
  against representative short strings, long prose, or CLI-sized inputs.

## Staged Refactor Plan

### PR 1: Establish Project Metadata and Development Bootstrap

Scope:

- Move static package metadata from `setup.py` into `pyproject.toml`.
- Add `requires-python` based on the versions the project intends to support.
- Add a development extra such as `.[dev]` with `pytest`, `flake8`, and build
  tooling.
- Keep `setup.py` only as a compatibility shim if needed.
- Fix README release wording so it matches the actual workflow.

Validation:

- Build an sdist and wheel.
- Install the wheel in a clean environment.
- Run tests through the documented dev command.

### PR 2: Harden CI Without Behavior Changes

Scope:

- Add a Python version matrix for supported versions.
- Add `python -m build` and package metadata checks to CI.
- Update GitHub Actions to current major versions.
- Keep the existing lint behavior initially to avoid mixing style churn with
  functional changes.

Validation:

- CI must pass on every supported Python version.
- Built artifacts should import `korean_romanizer` and expose `kroman`.

### PR 3: Define and Document the Stable API

Scope:

- Add `__all__` for the intended public package exports.
- Document `Romanizer` and `kroman` as stable APIs.
- Decide whether `Syllable`, `Pronouncer`, and module constants are supported or
  internal. If internal, document a deprecation policy before moving them.
- Add minimal docstrings for stable classes and functions.

Validation:

- Add import tests for the stable API.
- Add a compatibility note to README or a small API document.

### PR 4: Add Characterization Tests for Current Behavior

Scope:

- Convert example tests into a larger parameterized table.
- Add direct tests for `Syllable` decomposition/reconstruction and
  `Pronouncer` substitutions.
- Add tests for mixed scripts, punctuation, compatibility jamo, decomposed jamo,
  empty strings, and long text.
- Add known-bug tests as `xfail` for missing romanization rules.

Validation:

- No production behavior changes in this PR.
- Coverage should make later rule changes easy to review.

### PR 5: Internal Cleanup With No Intended Output Changes

Scope:

- Replace repeated output concatenation with list accumulation and `join`.
- Replace per-character regex calls with a helper such as `is_supported_hangul`.
- Rename constants to clearer internal names while preserving compatibility
  aliases where needed.
- Remove surprising side effects from `Syllable.__repr__`, keeping `__str__`
  behavior if required by existing code.
- Split pronunciation rules into small named helpers.

Validation:

- Characterization tests from PR 4 must pass unchanged.
- Add a small benchmark baseline before and after cleanup.

### PR 6: Improve Unicode Handling

Scope:

- Decide whether input should be normalized automatically, optionally, or left
  unchanged.
- Add support for modern decomposed jamo if it is in scope.
- Make unsupported jamo fallback behavior explicit and tested.

Validation:

- Add tests for NFC/NFD forms and compatibility jamo.
- Confirm existing precomposed Hangul outputs remain unchanged except where the
  PR intentionally fixes documented bugs.

### PR 7: Add Correctness Fixes in Small Rule-Focused PRs

Scope:

- Implement one phonological rule family per PR, starting with the highest-value
  known gaps:
  - palatalization such as `같이`;
  - nasal and liquid assimilation such as `종로`, `신라`, `울릉`, and `대관령`;
  - remaining double-final and `ㅎ` edge cases.
- Back each rule family with official examples or a checked golden corpus.
- Mark behavior-changing releases clearly.

Validation:

- Promote related `xfail` tests to passing tests.
- Add regression examples for every fixed case.

### PR 8: Modernize the CLI Contract

Scope:

- Add `--version`.
- Decide whether stdin support is desired when no positional text is provided.
- Decide whether whitespace should be preserved exactly or normalized by joining
  positional arguments with spaces.
- Document the CLI behavior.

Validation:

- Keep existing CLI behavior unless a release note calls out an intentional
  change.
- Test installed console script behavior from a built wheel.

### PR 9: Add Benchmarks and Performance Improvements

Scope:

- Add a lightweight benchmark script or pytest benchmark suite for short words,
  long prose, mixed text, and CLI-sized input.
- Optimize only after the no-behavior-change cleanup and correctness tests are
  in place.
- Consider reducing duplicate `Syllable` creation once the rule pipeline is well
  covered.

Validation:

- Compare benchmark output against the baseline from PR 5.
- Require equal or better correctness coverage before accepting speedups.

### PR 10: Harden Publishing

Scope:

- Move PyPI publishing to trusted publishing with `id-token: write`.
- Align release triggers with the documented process.
- Add artifact upload for release builds.
- Add a changelog or release notes checklist.

Validation:

- Test the workflow on TestPyPI or a dry-run build path before changing the
  production PyPI release process.
- Confirm `setuptools_scm` produces the intended version for tags and release
  builds.
