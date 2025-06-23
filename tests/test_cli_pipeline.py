# tests/test_cli_pipeline.py
import subprocess


def test_cli_help_exit_zero():
    res = subprocess.run(
        ["poetry", "run", "python", "cli/pipeline.py", "--help"],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert "Avvia la pipeline in modalità interattiva" in res.stdout
