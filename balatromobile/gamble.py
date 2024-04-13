
import subprocess
from argparse import ArgumentParser
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import shutil
from .resources import all_artifacts
from .patcher import all_patches


def main():
    # TODO: check if needed programs are installed
    # TODO: check programs exit status
    # TODO: more argparse options
    parser = ArgumentParser()
    parser.add_argument("BALATRO_EXE")
    args = parser.parse_args()
    balatro_exe = Path(args.BALATRO_EXE)
    artifacts = all_artifacts()
    patches = all_patches()
    if not balatro_exe.is_file():
        print("ERROR: invalid Balatro.exe")
        sys.exit(1)
    with TemporaryDirectory() as d:
        balatro = Path(d) / "Balatro"
        subprocess.run(["7za", "x", balatro_exe.absolute(), f"-o{balatro}"])
        for patch in [patches.basic, patches.landscape, patches.crt, patches.fps]:
            patch.apply(balatro)
        balatro_version = (balatro / "version.jkr").read_text().splitlines()[0]
        app = Path(d) / "balatro_app"
        subprocess.run(["java", "-jar", artifacts.apk_editor.absolute(), "d", "-i", artifacts.love_apk.absolute(), "-o", app.absolute()])
        manifest = artifacts.android_manifest.read_text().format(package='dev.bootkit.balatro', version=balatro_version, label="Balatro Mobile (unofficial)")
        (app / "AndroidManifest.xml").write_text(manifest)
        shutil.copytree(artifacts.android_res, app / "resources" / "package_1" / "res", dirs_exist_ok=True)
        subprocess.run(["7za", "a", "-tzip", (app / "root" / "assets" / "game.love").absolute()], cwd=balatro.absolute())
        apk = Path(d) / "balatro.apk"
        subprocess.run(["java", "-jar", artifacts.apk_editor.absolute(), "b", "-i", app.absolute(), "-o", apk.absolute()])
        subprocess.run(["java", "-jar", artifacts.apk_signer.absolute(), "-a", apk.absolute()])
        shutil.move(Path(d) / "balatro-aligned-debugSigned.apk", f"balatro-{balatro_version}.apk")

if __name__=="__main__":
    main()