from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import textwrap
import zipfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DIST_NAME = "korean_romanizer"
EXPECTED_DEV_REQUIRES = (
    "build>=1.2",
    "flake8>=7.0",
    "mypy>=1.10",
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "ruff>=0.6",
)


def run(command: list[str | Path], *, cwd: Path, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(part) for part in command],
        cwd=cwd,
        check=True,
        text=True,
        encoding="utf-8",
        capture_output=capture_output,
    )


def venv_path(venv_dir: Path, executable: str) -> Path:
    bin_dir = "Scripts" if os.name == "nt" else "bin"
    suffix = ".exe" if os.name == "nt" and executable in {"python", "kroman"} else ""
    return venv_dir / bin_dir / f"{executable}{suffix}"


def build_wheel(dist_dir: Path) -> Path:
    run([sys.executable, "-m", "build", "--wheel", "--outdir", dist_dir, PROJECT_ROOT], cwd=PROJECT_ROOT)
    wheels = sorted(dist_dir.glob(f"{DIST_NAME}-*.whl"))
    if len(wheels) != 1:
        raise AssertionError(f"Expected exactly one {DIST_NAME} wheel, found: {wheels}")
    return wheels[0]


def validate_wheel_contents(wheel_path: Path) -> None:
    with zipfile.ZipFile(wheel_path) as wheel:
        names = wheel.namelist()

    dist_info_prefixes = [name for name in names if name.startswith(f"{DIST_NAME}-") and ".dist-info/" in name]
    dist_info_roots = {name.split(".dist-info/", maxsplit=1)[0] + ".dist-info/" for name in dist_info_prefixes}
    if len(dist_info_roots) != 1:
        raise AssertionError(f"Expected exactly one {DIST_NAME} .dist-info tree, found: {sorted(dist_info_roots)}")

    dist_info_root = dist_info_roots.pop()
    allowed_prefixes = (f"{DIST_NAME}/", dist_info_root)

    if not any(name.startswith(f"{DIST_NAME}/") for name in names):
        raise AssertionError(f"Wheel does not contain the {DIST_NAME} package")

    unexpected = sorted(name for name in names if not name.startswith(allowed_prefixes))
    if unexpected:
        raise AssertionError(f"Wheel contains unexpected top-level files: {unexpected}")


def validate_installed_metadata(python: Path, work_dir: Path) -> None:
    metadata_check = textwrap.dedent(
        f"""
        import importlib.metadata as metadata
        import korean_romanizer
        from korean_romanizer import romanize

        dist = metadata.distribution("{DIST_NAME}")
        package_metadata = dist.metadata

        assert package_metadata["Name"] == "{DIST_NAME}", package_metadata["Name"]
        assert package_metadata["Requires-Python"] == ">=3.10", package_metadata["Requires-Python"]
        assert package_metadata["License-Expression"] == "GPL-3.0-or-later", package_metadata["License-Expression"]

        console_scripts = metadata.entry_points().select(group="console_scripts")
        kroman_scripts = [entry_point for entry_point in console_scripts if entry_point.name == "kroman"]
        assert len(kroman_scripts) == 1, kroman_scripts
        assert kroman_scripts[0].value == "korean_romanizer.cli:main", kroman_scripts[0].value

        extras = set(package_metadata.get_all("Provides-Extra") or [])
        assert "dev" in extras, extras

        requirements = package_metadata.get_all("Requires-Dist") or []
        expected_dev_requires = {EXPECTED_DEV_REQUIRES!r}
        for expected_requirement in expected_dev_requires:
            assert any(
                requirement.startswith(expected_requirement) and 'extra == "dev"' in requirement
                for requirement in requirements
            ), requirements

        assert korean_romanizer.romanize("안녕하세요") == "annyeonghaseyo"
        assert romanize("안녕하세요") == "annyeonghaseyo"
        """
    )
    run([python, "-c", metadata_check], cwd=work_dir)


def validate_console_script(kroman: Path, work_dir: Path) -> None:
    result = run([kroman, "안녕하세요"], cwd=work_dir, capture_output=True)
    output = result.stdout.strip()
    if output != "annyeonghaseyo":
        raise AssertionError(f"Expected kroman to output 'annyeonghaseyo', got {output!r}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="kroman-wheel-") as temp_dir:
        temp_path = Path(temp_dir)
        dist_dir = temp_path / "dist"
        venv_dir = temp_path / "venv"

        wheel_path = build_wheel(dist_dir)
        validate_wheel_contents(wheel_path)

        run([sys.executable, "-m", "venv", venv_dir], cwd=temp_path)
        python = venv_path(venv_dir, "python")
        kroman = venv_path(venv_dir, "kroman")

        run([python, "-m", "pip", "install", wheel_path], cwd=temp_path)
        validate_installed_metadata(python, temp_path)
        validate_console_script(kroman, temp_path)

        print(f"Validated {wheel_path.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
