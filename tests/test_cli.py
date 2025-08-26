import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from korean_romanizer.romanizer import Romanizer


UTF8_ENV = {**os.environ, "PYTHONIOENCODING": "UTF-8"}


def _run_cli(args, *, input=None):
    cmd = [sys.executable, "-m", "korean_romanizer.cli", *args]
    return subprocess.run(
        cmd,
        input=input,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        env=UTF8_ENV,
        timeout=10,
    )


@pytest.mark.parametrize(
    "text",
    [
        "안녕하세요",
        "아이유 방탄소년단",
        "구미, 영동",
        "구미,\t영동   서울!!",
    ],
)
def test_cli_matches_library(text):
    args = text.split()
    expected = Romanizer(" ".join(args)).romanize().strip()
    proc = _run_cli(args)
    assert proc.returncode == 0
    assert proc.stderr == ""
    assert proc.stdout.strip() == expected


def test_cli_help():
    proc = _run_cli(["-h"])
    assert proc.returncode == 0
    assert proc.stderr == ""
    assert "usage" in proc.stdout.lower()


@pytest.mark.parametrize("stdin", [None, "안녕하세요\n"])
def test_cli_no_args_shows_usage(stdin):
    proc = _run_cli([], input=stdin)
    assert proc.returncode != 0
    assert "usage" in proc.stderr.lower()


def test_cli_long_input():
    text = ("안녕하세요 " * 1000).strip()
    args = text.split()
    expected = Romanizer(" ".join(args)).romanize().strip()
    proc = _run_cli(args)
    assert proc.returncode == 0
    assert proc.stderr == ""
    assert proc.stdout.strip() == expected


def test_console_script_smoke():
    exe = shutil.which("kroman")
    if not exe:
        candidate = Path(sys.executable).with_name("kroman")
        if candidate.exists():
            exe = str(candidate)
    if not exe:
        candidate = Path(sys.executable).with_name("kroman.exe")
        if candidate.exists():
            exe = str(candidate)
    if not exe:
        pytest.skip("kroman console script not installed")
    proc = subprocess.run(
        [exe, "안녕하세요"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        env=UTF8_ENV,
        timeout=10,
    )
    expected = Romanizer("안녕하세요").romanize().strip()
    assert proc.returncode == 0
    assert proc.stderr == ""
    assert proc.stdout.strip() == expected
