import subprocess
from pathlib import Path

def run_silent(what: list[str], **kwargs):
    subprocess.run(
        what,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
        **kwargs
    )

def is_java_installed() -> bool:
    try:
        run_silent(["java", "-version"])
        return True
    except FileNotFoundError:
        return False

def get_balatro_version(balatro: Path) -> str:
    return (balatro / "version.jkr").read_text().splitlines()[0]