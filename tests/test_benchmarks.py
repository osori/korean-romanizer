import json
import os
import subprocess
import sys


UTF8_ENV = {**os.environ, "PYTHONIOENCODING": "UTF-8"}
EXPECTED_SCENARIOS = [
    "short_word",
    "sentence",
    "long_prose",
    "mixed_text",
    "cli_multiword",
]


def run_benchmark(*args):
    return subprocess.run(
        [sys.executable, "-m", "benchmarks.romanization", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        env=UTF8_ENV,
        timeout=20,
    )


def test_benchmark_cli_json_smoke():
    proc = run_benchmark("--warmup", "0", "--repeat", "1", "--loops", "1", "--json")

    assert proc.returncode == 0
    assert proc.stderr == ""

    payload = json.loads(proc.stdout)
    assert payload["benchmark"] == "romanization"
    assert payload["time_unit"] == "seconds"
    assert payload["warmup"] == 0
    assert payload["repeat"] == 1
    assert [result["name"] for result in payload["results"]] == EXPECTED_SCENARIOS
    assert all(result["loops"] == 1 for result in payload["results"])
    assert all(result["best_seconds"] <= result["median_seconds"] for result in payload["results"])


def test_benchmark_cli_human_smoke():
    proc = run_benchmark("--warmup", "0", "--repeat", "1", "--loops", "1")

    assert proc.returncode == 0
    assert proc.stderr == ""
    assert "Romanization benchmark baseline" in proc.stdout
    assert "median ms" in proc.stdout
    assert "short_word" in proc.stdout
