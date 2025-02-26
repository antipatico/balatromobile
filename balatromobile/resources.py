from argparse import Namespace
import  importlib.resources
import platform
from pathlib import Path

def get_resorce(basepath: str | Path, name: str | Path):
     with importlib.resources.as_file(importlib.resources.files(__package__)) as f:
        res = f / basepath / name
        if name is None or not res.exists():
            raise Exception(f'Missing resource: "{name}" in "{res.absolute()}"')
        return res

def get_artifact(name: str | Path) -> Path:
    return get_resorce("artifacts", name)

def get_patch(name: str | Path) -> Path:
    return get_resorce("patches", name)

def list_patches() -> list[str]:
    with importlib.resources.as_file(importlib.resources.files(__package__)) as f:
        return [f.stem for f in (f / "patches").glob("**/*.toml")]
    
def all_artifacts():
    os = platform.system().lower()
    arch = ({
        "x86_64": "amd64",
        "amd64": "amd64",
        "aarch64": "arm64",
        "arm64": "arm64",
    })[platform.machine().lower()]
    return Namespace(
        apk_editor = get_artifact("APKEditor-1.3.7.jar"),
        love_apk = get_artifact("love-11.5-SAF-android-embed.apk"),
        android_manifest = get_artifact("AndroidManifest.xml"),
        android_res = get_artifact("res"),
        zipalign = get_artifact(f"zipalign-{os}-{arch}"),
        uber_keystore = get_artifact("uber-debug.keystore"),
        apksigner = get_artifact("apksigner.jar"),
    )
