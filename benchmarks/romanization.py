from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from dataclasses import dataclass
from typing import Iterable

from korean_romanizer import romanize


# Hangul inputs are written with Unicode escapes so this benchmark remains
# ASCII-only and behaves consistently across terminals and shells.
LONG_PROSE = (
    "\ud55c\uad6d\uc5b4 \ub85c\ub9c8\uc790 \ud45c\uae30\ubc95\uc740 "
    "\ubc1c\uc74c\uacfc \ubb38\ub9e5\uc744 \ud568\uaed8 \ub2e4\ub8f9\ub2c8\ub2e4. "
)
LONG_PROSE_EXPECTED = "hangugeo romaja pyogibeobeun bareumgwa munmaegeul hamkke darupnida. "


@dataclass(frozen=True)
class Scenario:
    name: str
    description: str
    text: str
    expected: str
    loops: int


@dataclass(frozen=True)
class BenchmarkResult:
    name: str
    description: str
    characters: int
    loops: int
    median_seconds: float
    best_seconds: float


SCENARIOS = (
    Scenario(
        name="short_word",
        description="short Korean word",
        text="\ud55c\uae00",
        expected="hangeul",
        loops=5000,
    ),
    Scenario(
        name="sentence",
        description="normal Korean sentence",
        text=(
            "\uc548\ub155\ud558\uc138\uc694. \ud55c\uad6d\uc5b4 \ub85c\ub9c8\uc790 "
            "\ud45c\uae30\ubc95\uc785\ub2c8\ub2e4."
        ),
        expected="annyeonghaseyo. hangugeo romaja pyogibeobipnida.",
        loops=1000,
    ),
    Scenario(
        name="long_prose",
        description="long repeated Korean prose",
        text=LONG_PROSE * 200,
        expected=LONG_PROSE_EXPECTED * 200,
        loops=20,
    ),
    Scenario(
        name="mixed_text",
        description="mixed Korean/ASCII/punctuation text",
        text="Release 1.2: \uc548\ub155\ud558\uc138\uc694, Seoul! \ud14c\uc2a4\ud2b8=OK?",
        expected="Release 1.2: annyeonghaseyo, Seoul! teseuteu=OK?",
        loops=1000,
    ),
    Scenario(
        name="cli_multiword",
        description="CLI-sized multiword input",
        text=(
            "\uc11c\uc6b8 \ubd80\uc0b0 \ub300\uad6c \uc778\ucc9c "
            "\uad11\uc8fc \ub300\uc804 \uc6b8\uc0b0 \uc81c\uc8fc"
        ),
        expected="seoul busan daegu incheon gwangju daejeon ulsan jeju",
        loops=1000,
    ),
)


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("value must be at least 1")
    return parsed


def non_negative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("value must be 0 or greater")
    return parsed


def validate_expected_outputs(scenarios: Iterable[Scenario]) -> None:
    for scenario in scenarios:
        actual = romanize(scenario.text)
        if actual != scenario.expected:
            raise AssertionError(
                f"{scenario.name} expected {preview(scenario.expected)!r}, got {preview(actual)!r}"
            )


def preview(value: str, limit: int = 80) -> str:
    if len(value) <= limit:
        return value
    return f"{value[:limit]}..."


def time_batch(text: str, loops: int) -> float:
    romanize_text = romanize
    start = time.perf_counter()
    for _ in range(loops):
        romanize_text(text)
    return time.perf_counter() - start


def benchmark_scenario(
    scenario: Scenario,
    *,
    repeat: int,
    warmup: int,
    loops_override: int | None,
) -> BenchmarkResult:
    loops = loops_override if loops_override is not None else scenario.loops

    for _ in range(warmup):
        time_batch(scenario.text, loops)

    measurements = [time_batch(scenario.text, loops) for _ in range(repeat)]
    return BenchmarkResult(
        name=scenario.name,
        description=scenario.description,
        characters=len(scenario.text),
        loops=loops,
        median_seconds=statistics.median(measurements),
        best_seconds=min(measurements),
    )


def run_benchmarks(*, repeat: int, warmup: int, loops_override: int | None = None) -> list[BenchmarkResult]:
    validate_expected_outputs(SCENARIOS)
    return [
        benchmark_scenario(
            scenario,
            repeat=repeat,
            warmup=warmup,
            loops_override=loops_override,
        )
        for scenario in SCENARIOS
    ]


def render_text(results: Iterable[BenchmarkResult], *, repeat: int, warmup: int) -> str:
    lines = [
        "Romanization benchmark baseline",
        f"warmup={warmup} repeat={repeat} elapsed=batch",
        "",
        f"{'scenario':<15} {'description':<36} {'chars':>7} {'loops':>7} {'median ms':>10} {'best ms':>9}",
        "-" * 93,
    ]
    for result in results:
        lines.append(
            f"{result.name:<15} {result.description:<36} {result.characters:>7} {result.loops:>7} "
            f"{result.median_seconds * 1000:>10.3f} {result.best_seconds * 1000:>9.3f}"
        )
    return "\n".join(lines)


def render_json(results: Iterable[BenchmarkResult], *, repeat: int, warmup: int) -> str:
    payload = {
        "benchmark": "romanization",
        "time_unit": "seconds",
        "warmup": warmup,
        "repeat": repeat,
        "results": [
            {
                "name": result.name,
                "description": result.description,
                "characters": result.characters,
                "loops": result.loops,
                "median_seconds": round(result.median_seconds, 9),
                "best_seconds": round(result.best_seconds, 9),
            }
            for result in results
        ],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Benchmark korean_romanizer.romanize representative inputs.")
    parser.add_argument("--warmup", type=non_negative_int, default=2, help="warmup batches per scenario before timing")
    parser.add_argument("--repeat", type=positive_int, default=7, help="timed batches per scenario")
    parser.add_argument("--loops", type=positive_int, help="override each scenario's per-batch romanize calls")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of the human-readable table")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        results = run_benchmarks(repeat=args.repeat, warmup=args.warmup, loops_override=args.loops)
    except AssertionError as exc:
        print(f"Benchmark validation failed: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(render_json(results, repeat=args.repeat, warmup=args.warmup))
    else:
        print(render_text(results, repeat=args.repeat, warmup=args.warmup))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
