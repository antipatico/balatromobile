import tomllib
from pathlib import Path
from argparse import Namespace
from hashlib import sha256
from .resources import get_patch

DEFAULT_PATCHES = "basic,landscape,crt,fps"


class Patch:
    def __init__(self, patch: dict):
        self.target_file = patch["target_file"]
        self.hashes = patch["supported_hashes"]
        self.search_string = patch["search_string"]
        self.content = patch["patch_content"]

    def check_checksum(self, balatro: Path):
        target = balatro / Path(self.target_file)
        if not target.exists() or not target.is_file():
            return False
        if "skip" in self.hashes and len(self.hashes) == 1:
            return True
        hashsum = sha256(target.read_bytes()).hexdigest()
        return f"sha256:{hashsum[:10]}" in self.hashes
    
    def apply(self, balatro: Path):
        target = balatro / Path(self.target_file)
        patched = "\n".join([l if self.search_string not in l else self.content for l in target.read_text().splitlines()])
        target.write_text(patched)


class PatchList:
    def __init__(self, patch_list: list):
        self.patches = [Patch(p) for p in patch_list]
    
    def is_compatible(self, balatro: Path):
        return True # Disabling it for now, it may be sensible to save the game version instead. A problem is patching multiple times the save file.
        #return all(p.check_checksum(balatro) for p in self.patches)
    
    def apply_all(self, balatro: Path):
        for p in self.patches:
            p.apply(balatro)


class PatchFile:
    def __init__(self, filename):
        self.path = get_patch(filename)
        with open(self.path,"rb") as f:
            toml = tomllib.load(f)
        self.name : str = toml["name"]
        self.description : str = toml["description"]
        self.authors : list = toml["authors"]
        self.supported_platforms : list = toml["supported_platforms"]
        self.versions = {}
        for k, v in toml['versions'].items():
            self.versions[k] = PatchList(v)

    def supports_android(self) -> bool:
        return "android" in self.supported_platforms
    
    def supports_ios(self) -> bool:
        return "ios" in self.supported_platforms
    
    def __str__(self) -> str:
        return f'PatchFile(name="{self.name}", description="{self.description}", supported_platforms=[{",".join(self.supported_platforms)}])'

    def __repr__(self) -> str:
        return str(self)
    
    def apply(self, balatro: Path) -> str:
        for k, v in self.versions.items():
            if v.is_compatible(balatro):
                v.apply_all(balatro)
                return k
        raise Exception(f'Cannot find any compatible patch version with given Balatro.exe for {self}')


def all_patches() -> list[PatchFile]:
    return [
        PatchFile("basic.toml"),
        PatchFile("landscape.toml"),
        PatchFile("landscape-hidpi.toml"),
        PatchFile("crt.toml"),
        PatchFile("fps.toml"),
        PatchFile("external-storage.toml"),
    ]

def select_patches(patches: str) -> list[PatchFile]:
    patches = patches.split(",")
    return list(filter(lambda p: p.name in patches, all_patches()))
