# Changelog

## Unreleased

### Fixed

- Prevent `romanize()` and `Romanizer(...).romanize()` from raising `KeyError`
  when `ᆭ` or `ᆶ` meets a previously unsupported boundary, or when `ᇂ` is
  followed by initial `ㄹ`; the pronunciation layer now reduces the coda
  before romanization.
