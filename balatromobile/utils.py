import subprocess

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
        run_silent(["java", "--version"])
        return True
    except FileNotFoundError:
        return False