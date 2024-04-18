import tomllib
from pathlib import Path
from .resources import get_patch, get_artifact

DEFAULT_PATCHES = "basic,landscape,crt,fps"


class Patch:
    def __init__(self, patch: dict):
        self.search_string = patch.get("search_string", None)
        self.content = patch.get("patch_content", "")
        artifact_name = patch.get("artifact", None)
        self.artifact = get_artifact(artifact_name) if artifact_name is not None else None
        if self.search_string == self.artifact == None:
            raise Exception(f"Empty patches are not allowed")
    
    def apply(self, target_file: Path):
        target =target_file
        if self.artifact is not None:
            target.write_bytes(self.artifact.read_bytes())
            return
        patched = "\n".join([l if self.search_string not in l else self.content for l in target.read_text().splitlines()])
        target.write_text(patched)


class PatchFile:
    def __init__(self, patch_file: dict):
        self.target_file = Path(patch_file["target_file"])
        self.patches = [Patch(p) for p in patch_file["patches"]]
    
    def apply_all(self, balatro: Path):
        [p.apply(balatro / self.target_file) for p in self.patches]


class PatchList:
    def __init__(self, patch_list: dict):
        # Must be unique across patch lists to differentiate them
        self.version = patch_list['version']
        # If not defined, skip version checking
        self.supported_game_versions = patch_list.get('supported_game_versions', None) 
        self.patch_files = [PatchFile(p) for p in patch_list["patch_files"]]
    
    def is_compatible(self, version: str):
        return self.supported_game_versions is None or version in self.supported_game_versions
    
    def apply_all(self, balatro: Path):
        [p.apply_all(balatro) for p in self.patch_files]


class VersionedPatch:
    def __init__(self, name: str):
        self.path = get_patch(f"{name}.toml")
        with open(self.path,"rb") as f:
            toml = tomllib.load(f)
        self.name : str = name
        self.description : str = toml["description"]
        self.authors : list = toml["authors"]
        self.supported_platforms : list = toml["supported_platforms"]
        self.patch_lists = [PatchList(p) for p in toml['patch_lists']]

    def supports_android(self) -> bool:
        return "android" in self.supported_platforms
    
    def supports_ios(self) -> bool:
        return "ios" in self.supported_platforms
    
    def __str__(self) -> str:
        return f'VersionedPatch(name="{self.name}", description="{self.description}", supported_platforms=[{",".join(self.supported_platforms)}])'

    def __repr__(self) -> str:
        return str(self)
    
    def apply(self, balatro: Path, version: str) -> int:
        # TODO: allow user to specify specific patch version
        # TODO: allow user to force patch
        for p in self.patch_lists:
            if p.is_compatible(version):
                p.apply_all(balatro)
                return p.version
        raise Exception(f'Cannot find any compatible Patch version of "{self.name}" for given Balatro.exe having game version "{version}"')


def all_patches() -> list[VersionedPatch]:
    return [
        VersionedPatch("basic"),
        VersionedPatch("crt"),
        VersionedPatch("external-storage"),
        VersionedPatch("fps"),
        VersionedPatch("landscape-hidpi"),
        VersionedPatch("landscape"),
        VersionedPatch("no-background"),
        VersionedPatch("nunito-font"),
        VersionedPatch("simple-fx"),
        VersionedPatch("square-display"),
    ]

def select_patches(patches: str) -> list[VersionedPatch]:
    desired_patches = patches.split(",")
    patch_files : list[VersionedPatch] = list(filter(lambda p: p.name in desired_patches, all_patches()))
    if len(desired_patches) != len(patch_files):
        missing_patches = [p for p in desired_patches if p not in [P.name for P in patch_files]]
        raise Exception(f'One or more patches not found: {",".join(missing_patches)}')
    return patch_files