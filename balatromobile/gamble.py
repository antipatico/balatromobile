from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import shutil
from zipfile import ZipFile
from tabulate import tabulate

from .resources import all_artifacts
from .patcher import all_patches, select_patches, DEFAULT_PATCHES
from .utils import get_balatro_version, is_java_installed, run_silent
from .__version__ import __version__


def main():
    #TODO: iOS
    args = parse_args()
    if args.command == "android":
        android(args)
    elif args.command == "list-patches":
        list_patches(args)

def android(args: Namespace):
    balatro_exe = Path(args.BALATRO_EXE)
    artifacts = all_artifacts()
    patches = select_patches(args.patches)
    if sys.version_info.major == 3 and sys.version_info.minor < 11:
        print("WARNING: Python version < 3.11 is not tested and may not be supported")
    if not is_java_installed():
        print("ERROR: Java is not installed. Install Java-JRE before running this script")
        sys.exit(1)
    if not balatro_exe.is_file():
        print("ERROR: invalid Balatro.exe")
        sys.exit(1)
    with TemporaryDirectory() as d:
        balatro = Path(d) / "Balatro"
        with ZipFile(balatro_exe, "r") as z:
            z.extractall(balatro)
        balatro_version = get_balatro_version(balatro)
        for patch in patches:
            patch.apply(balatro, balatro_version, args.force)
        app = Path(d) / "balatro_app"
        run_silent(["java", "-jar", artifacts.apk_editor.absolute(), "d", "-i", artifacts.love_apk.absolute(), "-o", app.absolute()])
        manifest_tpl = artifacts.android_manifest.read_text()
        manifest = manifest_tpl.format(package=args.package_name, version=balatro_version, label=args.display_name)
        (app / "AndroidManifest.xml").write_text(manifest)
        shutil.copytree(artifacts.android_res, app / "resources" / "package_1" / "res", dirs_exist_ok=True)
        shutil.make_archive((Path(d) / "game.love").absolute(), "zip", balatro.absolute())
        shutil.move(Path(d) / "game.love.zip", (app / "root" / "assets" / "game.love"))
        apk = Path(d) / "balatro.apk"
        run_silent(["java", "-jar", artifacts.apk_editor.absolute(), "b", "-i", app.absolute(), "-o", apk.absolute()])
        output_apk = Path(args.output) if args.output else Path(f"balatro-{balatro_version}.apk")
        if args.skip_sign:
            shutil.move(apk.absolute(), output_apk.absolute())
        else:
            zipaligned_apk = Path(d) / "balatro-aligned.apk"
            run_silent([artifacts.zipalign.absolute(), "-i", apk.absolute(), "-o", zipaligned_apk.absolute()])
            signed_apk = Path(d) / "balatro-aligned-debugSigned.apk"
            run_silent([
                "java", "-jar", artifacts.apksigner.absolute(), "sign",
                "--ks-key-alias", "androiddebugkey",
                "--ks", artifacts.uber_keystore.absolute(),
                "--ks-pass", "pass:android",
                "--out", signed_apk.absolute(),
                zipaligned_apk.absolute()
            ])
            shutil.move(signed_apk, output_apk)

def list_patches(args: Namespace):
    print(tabulate(
        headers=["Name","Platforms", "Description", "Authors"],
        tabular_data=[[p.name, ",".join(p.supported_platforms), p.description, ",".join(p.authors)] for p in all_patches()]
    ))
    pass

def parse_args() -> Namespace:
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    commands = parser.add_subparsers(title='Commands', dest='command', required=True)
    # android
    android = commands.add_parser('android', help='Create an Android APK file')
    android.add_argument("BALATRO_EXE", help="Path to Balatro.exe file")
    android.add_argument("--output", "-o", required=False, help="Output path for apk (default: balatro-GAME_VERSION.apk)")
    android.add_argument("--patches", "-p", default=DEFAULT_PATCHES, help="Comma-separated list of patches to apply (default: %(default)s)")
    android.add_argument("--skip-sign", "-s", action="store_true", help="Skip signing the apk file with Uber Apk Signer (default: %(default)s)")
    android.add_argument("--display-name", default="Balatro Mobile (unofficial)", help="Change application display name (default: %(default)s)")
    android.add_argument("--package-name", default="dev.bootkit.balatro", help="Change application package name (default: %(default)s)")
    android.add_argument("--force", "-f", action="store_true", help="Force apply patches even if not compatible with supplied Balatro.exe version (default: %(default)s)")
    # list-patches
    android = commands.add_parser('list-patches', help='List available patches')
    return parser.parse_args()

if __name__=="__main__":
    main()
