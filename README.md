# <img src="misc/icon.png" width="60px"/> Balatro Mobile

Create a mobile version of Balatro from the Windows base version of the game. 

Python rewrite of [balatro-apk-maker](https://github.com/blake502/balatro-apk-maker) by [blake502](https://github.com/blake502) and friends. Compared to the original one, it is *NIX friendly, more modular, has patch versioning and does not try to download and install tools from the internet.

As of today, it only supports Android. Extending it to iOS should be trivial, if anyone is interested feel free to drop a PR!


## Prerequisites
This script comes pre-bundled with all the tools needed to make it work. The following list of programs must be installed to make the script work:
* [Java-JRE](https://www.java.com/en/download/manual.jsp)
* [Python >= 3.11](https://www.python.org/)

Moreover, you will need a copy of the game (buy it on [Steam](https://store.steampowered.com/app/2379780/Balatro/))

## Installation
Open a terminal and run
```bash
python3 -m pip install balatromobile
```

## Usage
```bash
balatromobile android Balatro.exe
```
This command will output an APK that is ready to be installed on your Android device.

## Save files
If your device is running Android 12 or prior, you will find your save files in your sdcard, more specifically under:
```
/sdcard/Android/data/dev.bootkit.balatro/
```

If your device is running Android 13 or later, you cannot access directly your files from your computer. Fortunately, you can use applications which supports the Storage Access Framework API (such as [FX File Explorer](https://play.google.com/store/apps/details?id=nextapp.fx) and [Material Files](https://play.google.com/store/apps/details?id=me.zhanghai.android.files)) to access the files from your device:

[![Video tut](misc/video-thumb-1.png)](https://vimeo.com/939997099 "Click to Watch!")

If you disable the `external-storage` patch, you can browse the game files using `run-as` in `adb`, for example:
```bash
adb shell run-as dev.bootkit.balatro ls
```
This is finnicky and error prone and not reccomended.

## Patches
Every patch is versioned, allowing the upkeeping of different patches for different versions of the game.
As of today, the platform check is disabled (since only android is supported anyway).
You can force the patching of unsupported game versions by supplying the `--force` flag.

You can list the available patches using the `list-patches` command:

```console
$ balatromobile list-patches
Name              Platforms    Description                                                                                      Authors
----------------  -----------  -----------------------------------------------------------------------------------------------  ---------------------------
basic             android      Basic set of patches needed to make the game run on mobile                                       blake502,TheCatRiX,PGgamer2
external-storage  android      Save game files under /sdcard/Android [Works well for Android < 13]                              blake502
fix-beta-langs    android,ios  Make beta langs selectable on mobile                                                             SBence,antipatico
fps               android,ios  Cap the FPS limit to the FPS limit of the screen                                                 PGgamer2
fps-settings      android,ios  Adds an FPS limit option to the graphics settings menu                                           janw4ld
landscape         android,ios  Forces the game to always stay in landscape mode, ignoring the screeen orentation of the device  blake502
landscape-hidpi   ios          Forces the game to always stay in landscape mode and apply hidpi fix for iOS                     blake502
max-volume        android,ios  Set master volume to 100 by default                                                              SBence
no-background     android,ios  Disable background animations and effects. From PortMaster                                       nkahoang,rancossack
no-crt            android,ios  Disable CRT effect [Fixes blackscreen bug on Pixels and other devices]                           blake502,SBence
nunito-font       android,ios  Replace the main font used with nunito, optimized for smaller displays. From PortMaster          nkahoang,rancossack
shaders-flames    android,ios  Fix the flames shaders for mobile                                                                PGgamer2
simple-fx         android,ios  Disable gameplay visible behind menu background, shadows, and bloom effects. From PortMaster     nkahoang,rancossack
square-display    android,ios  Optimize for square and square-like displays. From PortMaster                                    nkahoang,rancossack
```

It is possible to specify the list of patches you want to apply by supplying a comma-separated list of patches, for example:
```bash
balatromobile android Balatro.exe --patches basic,landscape,external-storage
```

## Supported Game Versions
* `1.0.1o-FULL`
* `1.0.1n-FULL`
* `1.0.1m-FULL`
* `1.0.1g-FULL`
* `1.0.1f-FULL`
* `1.0.1e-FULL` (public beta)
* `1.0.1c-FULL` (public beta)

## Advanced Usage
```
$ balatromobile android -h
usage: balatromobile android [-h] [--output OUTPUT] [--patches PATCHES] [--skip-sign] [--display-name DISPLAY_NAME] [--package-name PACKAGE_NAME] [--force]
                             BALATRO_EXE

positional arguments:
  BALATRO_EXE           Path to Balatro.exe file

options:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Output path for apk (default: balatro-GAME_VERSION.apk)
  --patches PATCHES, -p PATCHES
                        Comma-separated list of patches to apply (default: basic,landscape,no-crt,fps,external-storage,shaders-flames,fix-beta-langs,
                        max-volume)
  --skip-sign, -s       Skip signing the apk file with Uber Apk Signer (default: False)
  --display-name DISPLAY_NAME
                        Change application display name (default: Balatro Mobile (unofficial))
  --package-name PACKAGE_NAME
                        Change application package name (default: dev.bootkit.balatro)
  --force, -f           Force apply patches even if not compatible with supplied Balatro.exe version (default: False)
```

## Credits
This software is a rewrite of [balatro-apk-maker](https://github.com/blake502/balatro-apk-maker). It uses [APKEditor](https://github.com/REAndroid/APKEditor), [Love Android](https://github.com/love2d/love-android) and [Nunito Font](https://fonts.google.com/specimen/Nunito). Moreover, some patches were ported from [nkaHong's fork of PortMaster](https://github.com/nkahoang/PortMaster-nkaHoang).

Thanks for everybody contributing to this project.
