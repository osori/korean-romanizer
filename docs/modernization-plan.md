# Modernization Plan

This plan covers the `korean-romanizer` Python package in this repository. It
is current as of PR #53 and reflects the source tree, tests, packaging metadata,
and GitHub Actions workflows on `master`.

## Current Architecture

The project is a small, dependency-free Python package that romanizes Hangul
text using a rule-based pipeline:

1. `korean_romanizer.romanizer.romanize(text)` is the preferred public library
   flow. It sends text through pronunciation normalization, then romanizes the
   pronounced characters.
2. `korean_romanizer.pronouncer.Pronouncer` builds a list of `Syllable` objects
   for the input text and applies context-sensitive pronunciation
   substitutions. It mutates adjacent `Syllable` instances in place, then
   exposes the resulting string through `pronounced`.
3. `korean_romanizer.syllable.Syllable` decomposes a single precomposed Hangul
   syllable into initial, medial, and final jamo using Unicode arithmetic. It
   can also reconstruct the syllable after those pieces are mutated.
4. `korean_romanizer.romanizer.Romanizer` is a backward-compatible wrapper
   around the functional API. `Romanizer(text).romanize()` returns
   `romanize(text)`.
5. `korean_romanizer.cli` is a thin `argparse` wrapper. It joins positional
   arguments with spaces, romanizes that string through `romanize(text)`, and
   prints the result.

The package uses a flat source layout, not a `src/` layout. The core tables and
rules live in module globals rather than structured data files. There are no
runtime dependencies.

## Public API Surface

The preferred public API is:

- `from korean_romanizer import romanize`
- `romanize(text) -> str`
- the `kroman` console script

Compatibility APIs remain supported:

- `from korean_romanizer import Romanizer`
- `from korean_romanizer.romanizer import Romanizer`
- `Romanizer(text).romanize()`
- `from korean_romanizer import Pronouncer, Syllable`

`korean_romanizer.__all__` is explicit and currently contains only
`romanize`, `Romanizer`, `Pronouncer`, and `Syllable`. Wildcard imports follow
that contract. `Pronouncer` and `Syllable` are lower-level compatibility exports
because earlier releases made them importable; refactors should preserve them
unless a deprecation path is documented and tested first.

Module-level constants, tables, and helper functions are implementation
details. Some remain importable for historical reasons, so changes to them
should still be treated carefully, but new application code should not depend
on them. Public API narrowing should be intentional, documented, tested, and
called out in release notes.

## Existing Tests and Gaps

Current tests:

- `tests/test_romanizer.py` retains the original/basic example coverage,
  including onset/coda mappings and final-consonant behavior.
- `tests/test_characterization.py` snapshots existing behavior for mixed text,
  whitespace, compatibility jamo, `Pronouncer`, and `Syllable`.
- `tests/test_unicode_characterization.py` snapshots current NFC/NFD,
  decomposed modern jamo, compatibility-jamo decomposition, mixed text,
  whitespace, and unsupported archaic-jamo behavior.
- `tests/test_rr_correctness.py` contains source-backed Revised Romanization
  rule fixtures.
- `tests/test_public_api.py` locks the preferred and compatibility APIs,
  package exports, `__all__`, and wildcard-import behavior.
- `tests/test_cli.py` checks that `python -m korean_romanizer.cli` matches the
  library for several inputs, prints help, errors on missing arguments, handles
  a long argument list, supports `--version`, and smoke-tests the installed
  `kroman` console script when available.
- `tests/test_benchmarks.py` smoke-tests the dependency-free benchmark CLI in
  human-readable and JSON modes.
- CI installs the package with `python -m pip install -e ".[dev]"`, runs pytest
  on Python 3.10, 3.11, 3.12, and 3.13, and runs quality gates on Python 3.10.

Observed test gaps:

- `Syllable` and `Pronouncer` have more direct coverage than the original plan,
  but the pronunciation rule pipeline still depends heavily on ordered mutation
  and should gain focused helper-level tests before helper behavior changes.
- There is no full golden corpus from the official Revised Romanization rules or
  from checked dictionary examples.
- Unicode normalization behavior is characterized, but the project still needs
  an explicit policy decision before changing NFC/NFD, decomposed-jamo, or
  archaic-jamo behavior. Invalid input types and very large text still need
  explicit coverage.
- The CLI tests intentionally join arguments with spaces, but do not define
  whether preserving original whitespace is part of the long-term contract.

## CI, Packaging, and Release Setup

Current CI:

- `.github/workflows/python-app.yml` runs on pushes and pull requests against
  `master`.
- The test matrix covers Python 3.10, 3.11, 3.12, and 3.13.
- The quality-gates job runs `ruff check .`, `mypy korean_romanizer`,
  `python -m build`, and `python scripts/validate_wheel_metadata.py`.
- The wheel validator builds a wheel, checks the wheel contents, installs it in
  a temporary virtual environment, validates emitted metadata, imports the
  package, exercises `romanize(text)`, and smoke-tests the installed `kroman`
  console script.

Current packaging:

- `pyproject.toml` uses PEP 621 `[project]` metadata.
- `requires-python` is `>=3.10`, and Python classifiers match the CI matrix.
- Versions remain dynamic and are derived from Git tags through
  `setuptools_scm`.
- The `dev` extra contains the local test, lint, type-check, coverage, and build
  tooling.
- The `kroman` entry point is declared under `[project.scripts]`.
- Package inclusion remains explicit under `[tool.setuptools]`.
- `setup.py` is a minimal `setuptools.setup()` compatibility shim.

Release setup:

- `.github/workflows/python-publish.yml` builds with `python -m build` and
  publishes to PyPI using `pypa/gh-action-pypi-publish` when a GitHub release is
  published.
- The README now documents that publishing path.
- The publish workflow still uses a PyPI API token secret rather than PyPI
  trusted publishing through OpenID Connect.
- The publish workflow still uses older `actions/checkout` and
  `actions/setup-python` major versions.

## Likely Correctness Risks

- The implementation does not cover all Revised Romanization edge cases.
  Liquid/nasal assimilation, palatalization, and the source-backed h-adjacency
  family have moved into RR correctness coverage, but remaining rule families
  should continue to be fixed in small, source-backed PRs.
- Decomposed modern jamo are not consistently romanized because the romanizer
  supports precomposed Hangul and compatibility jamo, not the modern
  choseong/jongseong Unicode blocks.
- The algorithm has no morphology or word-boundary model. Some Korean
  romanization rules depend on morpheme boundaries, proper nouns, names, or
  conventional spellings, which a pure character-neighborhood pass cannot infer.
- Revised Romanization includes transcription special provisions that are not
  pure pronunciation rules. The current implementation should treat
  source-backed examples as guarded compatibility data until a dedicated
  proper-name or administrative-unit layer exists.
- Proper nouns should probably not be handled by hidden guesses in the core
  transliterator. A safer approach is an optional override layer: keep the
  default algorithm deterministic, then allow callers or a curated data file to
  supply accepted spellings for names, places, and brand terms.
- `Pronouncer.final_substitute` mutates adjacent syllables in place and depends
  on rule order. The major rule blocks now dispatch to private helpers, but
  helper edits or new rule families still need characterization tests to avoid
  silent behavior changes.
- `Syllable.__repr__` reconstructs and mutates `self.char`, which is surprising
  for a representation method and could make debugging or future caching
  behavior confusing.
- Some mappings appear inconsistent or dead, such as double-final data that has
  compatibility-jamo and full-syllable-final edge cases.
- `Romanizer` assumes pronunciation normalization has reduced all finals to the
  codas represented in `coda`. Missed substitutions can become `KeyError`
  failures instead of graceful fallback behavior.

## Performance Risks

- Romanization is linear in input size conceptually, but it does two character
  passes and creates `Syllable` objects in `Pronouncer` and the romanization
  pass.
- `Pronouncer` reconstructs a full pronounced string before romanization. A
  future streaming or single-pass design could avoid intermediate strings, but
  should come after correctness characterization.
- A dependency-free benchmark baseline now covers short words, a sentence, long
  repeated prose, mixed text, and CLI-sized multiword input. It is intended for
  local before/after comparisons, not committed machine-specific timing results
  or CI thresholds.

## Progress Since Plan Creation

Status as of 2026-06-22:

- PR #31 added the local development bootstrap and documented dev commands.
- PR #32 hardened CI with the supported Python matrix, linting, type checks, and
  package build validation.
- PR #33 added characterization coverage for existing behavior.
- PR #34 simplified internal romanizer character handling, including list-based
  output accumulation and direct Hangul range checks.
- PR #35 cleaned up packaging metadata warnings.
- PR #36 organized romanization tables while preserving compatibility exports.
- PR #37 fixed source-backed RR liquid/nasal assimilation examples.
- PR #39 fixed source-backed RR palatalization examples.
- PR #40 fixed the source-backed h-adjacency example and the related inflection
  family while retaining noun guards for compatibility examples.
- PR #42 added `romanize(text)` as the preferred public API, kept
  `Romanizer(text).romanize()` as the compatibility API, documented the
  compatibility policy, and locked the explicit `__all__` contract.
- PR #43 moved static package metadata into PEP 621 metadata in
  `pyproject.toml`, kept SCM-derived dynamic versioning, moved the `dev` extra
  and `kroman` script into project metadata, reduced `setup.py` to a minimal
  shim, and added wheel metadata validation to CI.
- PR #46 extracted representative-final pronunciation substitutions into a
  private helper.
- PR #47 extracted final-`h` pronunciation substitutions into a private helper.
- PR #48 extracted double-final vowel-linking substitutions into a private
  helper.
- PR #49 added Unicode characterization coverage for NFC precomposed Hangul,
  equivalent NFD pass-through behavior, decomposed modern jamo, compatibility
  jamo decomposition, mixed normalized text, punctuation/whitespace preservation,
  and unsupported archaic-jamo pass-through behavior.
- PR #50 added `kroman --version` and tests for both module and installed
  console-script execution.
- PR #51 added the dependency-free `benchmarks.romanization` baseline with
  scenarios for short words, normal sentences, long repeated prose, mixed text,
  and CLI-sized multiword input, plus smoke tests for JSON and human-readable
  output.
- PR #52 extracted liquid/nasal assimilation substitutions into a private
  helper.
- PR #53 extracted single-final vowel-linking substitutions into a private
  helper. Together with PRs #46, #47, #48, and #52, all current pronunciation
  rule blocks in `Pronouncer.final_substitute` now dispatch through private
  helpers while preserving rule order and public behavior.

The next implementation step should be a compatibility-safe `Syllable.__repr__`
cleanup. It should first add focused characterization tests for current
representation side effects, then remove the surprising `self.char` mutation
only if public behavior remains intentionally preserved or the change is
explicitly documented.

## Staged Refactor Plan

### PR 1: Establish Project Metadata and Development Bootstrap

Status: Complete.

Completed scope:

- Static package metadata moved from `setup.py` into PEP 621 metadata in
  `pyproject.toml`.
- `requires-python` is `>=3.10`.
- The `dev` extra documents and installs local development tooling.
- `setup.py` is only a minimal compatibility shim.
- README release wording matches the current GitHub-release publishing trigger.

Remaining follow-up:

- Publishing hardening belongs in PR 10, not this stage.

### PR 2: Harden CI Without Behavior Changes

Status: Complete.

Completed scope:

- CI runs the supported Python 3.10-3.13 test matrix.
- Quality gates run ruff, mypy, package build, and wheel validation.
- GitHub Actions for the application workflow use current checkout and
  setup-python major versions.
- Built artifacts are validated for package contents, installed metadata,
  `romanize(text)`, and `kroman`.

### PR 3: Define and Document the Stable API

Status: Complete.

Completed scope:

- `romanize(text)` is the preferred public API.
- `Romanizer(text).romanize()` remains the compatibility API.
- `Pronouncer` and `Syllable` remain lower-level compatibility exports.
- `__all__` explicitly defines wildcard-import behavior.
- Constants, tables, and helper functions are documented as internal
  implementation details.
- Import and wildcard behavior are covered by tests.

### PR 4: Add Characterization Tests for Current Behavior

Status: Substantially complete.

Completed scope:

- Existing romanizer examples were expanded into broader characterization and
  RR-correctness coverage.
- Public API, CLI, mixed text, compatibility jamo, and selected rule families
  have regression coverage.
- Unicode normalization behavior and unsupported jamo pass-through behavior are
  now covered by characterization tests.
- Several known RR examples have moved from gaps into passing source-backed
  tests.

Remaining scope:

- Add more direct helper-level tests before changing order-sensitive
  `Pronouncer` helper behavior.
- Add invalid-input and large-text characterization.
- Expand Unicode tests only when the project chooses a desired normalization
  policy beyond the current behavior snapshots.
- Build a checked golden corpus if the project wants broader RR conformance
  claims.

### PR 5: Internal Cleanup With No Intended Output Changes

Status: Substantially complete.

Completed scope:

- Romanizer output now uses list accumulation and `join`.
- Per-character regex matching was replaced with direct Hangul range checks.
- Some table organization has already landed while preserving compatibility
  exports.
- The representative-final, final-`h`, double-final vowel-linking,
  liquid/nasal assimilation, and single-final vowel-linking rule blocks now live
  in private helper functions.

Later scope:

- Rename internal constants only where compatibility aliases are preserved.
- Remove surprising side effects from `Syllable.__repr__`, preceded by focused
  characterization tests and keeping compatibility risks explicit.
- Use the benchmark baseline before performance-motivated changes.

### PR 6: Improve Unicode Handling

Status: Partial.

Completed scope:

- Current Unicode normalization behavior is characterized for NFC precomposed
  Hangul, equivalent NFD pass-through behavior, decomposed modern jamo,
  compatibility-jamo decomposition, mixed normalized text, whitespace, and
  unsupported archaic jamo.

Scope:

- Decide whether input should be normalized automatically, optionally, or left
  unchanged.
- Add support for modern decomposed jamo if it is in scope.
- Make unsupported jamo fallback behavior explicit and tested.

Validation:

- Keep the current NFC/NFD and compatibility-jamo characterization tests passing
  unless a PR intentionally changes and documents the contract.
- Confirm existing precomposed Hangul outputs remain unchanged except where the
  PR intentionally fixes documented bugs.

### PR 7: Add Correctness Fixes in Small Rule-Focused PRs

Status: Partial.

Completed scope:

- Source-backed liquid/nasal assimilation examples landed in PR #37.
- Source-backed palatalization examples landed in PR #39.
- A source-backed h-adjacency family landed in PR #40.

Remaining scope:

- Continue with one phonological rule family per PR.
- Back each rule family with official examples or a checked golden corpus.
- Keep standard-pronunciation fixes separate from RR special provisions for
  proper names and administrative units.
- Mark behavior-changing releases clearly.

Validation:

- Promote related `xfail` tests to passing tests.
- Add regression examples for every fixed case.

### PR 8: Modernize the CLI Contract

Status: Partial: `--version` complete; stdin and whitespace decisions pending.

Completed scope:

- `kroman --version` prints the installed distribution version.
- Module and console-script version behavior is covered by tests.

Scope:

- Decide whether stdin support is desired when no positional text is provided.
- Decide whether whitespace should be preserved exactly or normalized by joining
  positional arguments with spaces.
- Document the CLI behavior.

Validation:

- Keep existing CLI behavior unless a release note calls out an intentional
  change.
- Test installed console script behavior from a built wheel.

### PR 9: Add Benchmarks and Performance Improvements

Status: Partial: benchmark baseline complete; optimizations pending.

Completed scope:

- Added `python -m benchmarks.romanization` with dependency-free benchmark
  scenarios for short words, a sentence, long repeated prose, mixed text, and
  CLI-sized multiword input.
- Added human-readable and JSON output modes.
- Added benchmark smoke tests that validate expected outputs before timing.

Scope:

- Optimize only after the no-behavior-change cleanup and correctness tests are
  in place.
- Consider reducing duplicate `Syllable` creation once the rule pipeline is well
  covered.

Validation:

- Compare benchmark output against the existing baseline before and after any
  performance-motivated change.
- Require equal or better correctness coverage before accepting speedups.

### PR 10: Harden Publishing

Status: Pending.

Scope:

- Move PyPI publishing to trusted publishing with `id-token: write`.
- Update the publish workflow to current action major versions.
- Add artifact upload for release builds.
- Add a changelog or release notes checklist.

Validation:

- Test the workflow on TestPyPI or a dry-run build path before changing the
  production PyPI release process.
- Confirm `setuptools_scm` produces the intended version for tags and release
  builds.

### PR 11: Prepare a v1.0.x Release

Status: Future.

Scope:

- Decide the minimum public API and behavior guarantees for the first stable
  release.
- Review any remaining known correctness gaps and either fix them, document
  them, or mark them as explicitly out of scope for 1.0.
- Freeze the compatibility policy for `romanize(text)`, `Romanizer`, `kroman`,
  and any supported lower-level imports.
- Cut the first `v1.0.x` release only after CI, packaging, and release
  automation are reliable.

Validation:

- Run the full supported Python matrix.
- Build and inspect release artifacts.
- Publish through the hardened release workflow.
