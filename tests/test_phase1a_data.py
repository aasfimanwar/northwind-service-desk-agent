import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _run(script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "tools" / script)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_generator_is_deterministic() -> None:
    manifest = ROOT / "data" / "MANIFEST.json"
    before = manifest.read_bytes()
    result = _run("gen_company.py")
    assert result.returncode == 0, result.stderr
    assert manifest.read_bytes() == before


def test_phase1a_validator_passes() -> None:
    generated = _run("gen_company.py")
    assert generated.returncode == 0, generated.stderr
    result = _run("validate_phase1a.py")
    assert result.returncode == 0, result.stdout
