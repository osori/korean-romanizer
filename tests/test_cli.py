import os
import shutil
import subprocess
import sys

import pytest
from korean_romanizer.romanizer import Romanizer


def _run_cli(args):
    env = {**os.environ, "PYTHONIOENCODING": "UTF-8"}
    cmd = [sys.executable, "-m", "korean_romanizer.cli", *args]
    return subprocess.run(cmd, capture_output=True, text=True, check=False, env=env)


@pytest.mark.parametrize("text", [
    "안녕하세요",
    "아이유 방탄소년단",
    "구미, 영동",
])
def test_cli_matches_library(text):
    expected = Romanizer(text).romanize().strip()
    args = text.split()
    proc = _run_cli(args)
    assert proc.returncode == 0
    assert proc.stdout.strip() == expected


def test_cli_help():
    proc = _run_cli(["-h"])
    assert proc.returncode == 0
    assert "usage" in proc.stdout.lower()


def test_console_script_smoke():
    exe = shutil.which("kroman")
    if not exe:
        pytest.skip("kroman console script not installed")
    env = {**os.environ, "PYTHONIOENCODING": "UTF-8"}
    proc = subprocess.run([exe, "안녕하세요"], capture_output=True, text=True, check=False, env=env)
    expected = Romanizer("안녕하세요").romanize().strip()
    assert proc.returncode == 0
    assert proc.stdout.strip() == expected
