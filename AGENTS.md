# AGENTS.md

## Project Goal

This is a Python library and CLI for Korean Revised Romanization. Preserve
existing public behavior unless a change is explicitly documented, tested, and
called out in release notes.

## Repository Map

- `korean_romanizer/romanizer.py`: public `Romanizer(text).romanize()` flow and
  romanization tables.
- `korean_romanizer/pronouncer.py`: context-sensitive pronunciation
  substitutions before romanization.
- `korean_romanizer/syllable.py`: Hangul syllable decomposition and
  reconstruction helpers.
- `korean_romanizer/cli.py`: `kroman` console entry point.
- `tests/`: pytest coverage for library and CLI behavior.
- `docs/modernization-plan.md`: staged modernization notes and known risks.

## Commands

Set up a local development checkout:

- Install dev tooling: `python3 -m pip install -e ".[dev]"`

- Run tests: `python3 -m pytest`
- Run CLI smoke test: `python3 -m korean_romanizer.cli 안녕하세요`
- Run coverage: `python3 -m pytest --cov=korean_romanizer`
- Run linting: `ruff check .`
- Format code only in a dedicated formatting PR: `ruff format .`
- Run type checks: `mypy korean_romanizer`
- Build package: `python3 -m build`

## Rules

- Do not change romanization behavior without adding regression tests.
- Keep `Romanizer(text).romanize()` backward compatible.
- Keep the `kroman` console script backward compatible unless a CLI contract
  change is explicitly documented and tested.
- Prefer small PRs with one purpose.
- For rule changes, add a focused test fixture and a short comment or reference
  explaining the Korean pronunciation or romanization rule being implemented.
- Treat `Syllable`, `Pronouncer`, and module-level tables as compatibility risks
  until the public API surface is explicitly narrowed or documented.
- Preserve mixed non-Korean text and punctuation behavior unless changing it is
  intentional and tested.
- Include before/after benchmark numbers for performance-related changes.
- Do not mix packaging, formatting, and romanization rule changes in one PR.
- Avoid broad refactors until characterization tests cover the current behavior.
