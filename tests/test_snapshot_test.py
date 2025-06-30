# test_snapshot_test.py
import pytest
from typer import Exit

from audit import snapshot_test


def test_snapshot_test_exits_on_missing_snapshot(monkeypatch):
    # Monkeypatch diretto su funzione importata
    monkeypatch.setattr(
        snapshot_test, "find_latest_snapshot_paths", lambda: (None, None)
    )

    with pytest.raises(Exit) as exc_info:
        snapshot_test.snapshot_test(ci_mode=False)

    assert exc_info.value.exit_code == 1
