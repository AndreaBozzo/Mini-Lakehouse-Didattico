# scripts/update_readme.py

import re
import subprocess
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer()
console = Console()
README_PATH = Path("README.md")

SECTIONS = {
    "DIAGRAM": Path("docs/architecture.mmd"),
    "STRUCTURE": "TREE",
    "CHANGELOG": "GIT",  # opzionale in futuro
}


def replace_section(content: str, section: str, replacement: str) -> str:
    pattern = rf"(<!-- AUTO-SECTION:{section} -->)(.*?)(<!-- END-SECTION:{section} -->)"
    repl = rf"\1\n\n{replacement.strip()}\n\n\3"
    return re.sub(pattern, repl, content, flags=re.DOTALL)


def generate_changelog() -> str:
    try:
        tags = subprocess.check_output(
            ["git", "tag", "--sort=-creatordate"], text=True
        ).splitlines()

        blocks = []
        for tag in tags:
            tag_msg = (
                subprocess.run(
                    ["git", "tag", "-n", tag], text=True, capture_output=True
                )
                .stdout.strip()
                .split(maxsplit=1)[-1]
            )
            log = subprocess.run(
                ["git", "log", f"{tag}^!", "--oneline"], text=True, capture_output=True
            ).stdout.strip()

            commit_lines = "\n".join(f"- {line}" for line in log.splitlines())
            blocks.append(f"### {tag}\n> {tag_msg}\n\n{commit_lines}\n")

        return "\n".join(blocks) if blocks else "_Nessun tag trovato._"
    except subprocess.CalledProcessError:
        return "_Errore durante la generazione del changelog._"


def generate_project_structure() -> str:
    def list_dir(path: Path, level=0, max_level=2):
        if level > max_level:
            return ""
        lines = []
        for item in sorted(path.iterdir()):
            if item.name.startswith(".") or item.name in ("__pycache__", ".venv"):
                continue
            indent = "│   " * level + "├── "
            lines.append(f"{indent}{item.name}")
            if item.is_dir():
                sub = list_dir(item, level + 1, max_level)
                if sub:
                    lines.append(sub)
        return "\n".join(lines)

    output = list_dir(Path("."))
    return f"```bash\n{output}\n```"


@app.command()
def main(ci_mode: bool = typer.Option(False, help="Modalità silenziosa per CI")):
    original = README_PATH.read_text(encoding="utf-8")
    updated = original

    for section, source in SECTIONS.items():
        if source == "GIT":
            section_content = generate_changelog()
        elif source == "TREE":
            section_content = generate_project_structure()
        else:
            path = Path(source)
            if not path.exists():
                if not ci_mode:
                    console.print(f"[yellow]⚠️  File mancante:[/yellow] {path}")
                continue
            section_content = f"```\n{path.read_text(encoding='utf-8').strip()}\n```"

        updated = replace_section(updated, section, section_content)

    if updated != original:
        README_PATH.write_text(updated, encoding="utf-8")
        if not ci_mode:
            console.print("[green]✅ README.md aggiornato con successo.[/green]")
    else:
        if not ci_mode:
            console.print("[blue]ℹ️ Nessuna modifica necessaria al README.[/blue]")


if __name__ == "__main__":
    app()
