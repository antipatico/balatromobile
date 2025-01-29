import subprocess
from os import environ
from pathlib import Path

DEBUG = (debug := environ.get("BALATROMOBILE_DEBUG")) and (debug.lower() != "false")

def run_silent(what: list[str], **kwargs):
    outpipe = subprocess.DEVNULL

    if DEBUG:
        from sys import stderr
        print(f"[DEBUG] `run_silent`: {what=}", file=stderr)
        outpipe = stderr

    subprocess.run(
        what,
        stdin=subprocess.DEVNULL,
        stdout=outpipe,
        stderr=outpipe,
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
