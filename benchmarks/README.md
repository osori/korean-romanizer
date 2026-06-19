# Romanization Benchmarks

This directory contains a dependency-free benchmark baseline for the public
`korean_romanizer.romanize()` API. It uses only the Python standard library.

Run it from the repository root:

```console
python -m benchmarks.romanization
```

The benchmark validates every scenario's expected output before timing, runs
warmup batches, then reports the median and best elapsed batch time.

Useful options:

```console
python -m benchmarks.romanization --json
python -m benchmarks.romanization --warmup 3 --repeat 10
python -m benchmarks.romanization --loops 100
```

The default human-readable output is intended for local before/after
comparisons. Do not commit machine-specific timing results, add performance
thresholds, or wire this benchmark into CI.
