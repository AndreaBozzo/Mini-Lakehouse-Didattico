# cli/core.py

from cli.utils import run_step


def run_pipeline(real_data: bool = False, ci_mode: bool = False, verbose: bool = False):
    """Esegue la pipeline ETL: run dbt + test + docs."""
    suffix = "tag:real" if real_data else "tag:simulated"

    steps = [
        ("Clean", "poetry run dbt clean"),
        ("Deps", "poetry run dbt deps"),
        *([] if real_data else [("Seed", "poetry run dbt seed")]),
        ("Run", f"poetry run dbt run --select {suffix}"),
        ("Test", f"poetry run dbt test --select {suffix}"),
        ("Docs", "poetry run dbt docs generate"),
    ]

    for name, cmd in steps:
        run_step(name, cmd)


def export_marts(real_data: bool = False, ci_mode: bool = False, verbose: bool = False):
    """Esporta i marts in CSV e Parquet."""
    cmd = "poetry run python audit/export_marts.py"
    if verbose:
        cmd += " --verbose"
    run_step("Export marts", cmd)


def audit_log(ci_mode: bool = False):
    """Confronta gli snapshot attuali con quelli precedenti."""
    cmd = "poetry run python -m cli.pipeline snapshot"
    if ci_mode:
        cmd += " --ci-mode"
    run_step("Snapshot check", cmd)


def post_checks():
    """Esegue i controlli di qualità finale."""
    run_step("Coverage", "make coverage")
    run_step("Quality Report", "make quality-report")
