# <img src="icon.png" width="60px"/> Balatro Mobile

Create a mobile version of Balatro from the Windows base game. 

Python fork of [balatro-apk-maker](https://github.com/blake502/balatro-apk-maker) by [blake502](https://github.com/blake502) and friends. Compared to the original one, it is *NIX friendly, more modular, has patch versioning and does not need to download tools from the internet.

As of today, it only supports Android, but estending it to iOS should be trivial.


## Prerequisites
This script comes pre-bundled with all the tools needed to make it work. The following list of programs must be installed to make the script work:
* [7zip](https://www.7-zip.org/)
* [Java-JRE](https://www.java.com/en/download/manual.jsp)
* [Python >= 3.11](https://www.python.org/)

Moreover, you will need a copy of the game (buy it on [Steam](https://store.steampowered.com/app/2379780/Balatro/))

## Installation
Open a terminal and run
```bash
python3 -m pip install balatromobile
```

**NOTE**: the package as no dependencies, you can install it in any venv without any problem.

## Usage
```bash
balatromobile Balatro.exe
```
This command will output an APK with all needed patches and already signed. Ready to be installed on your Android device.

## Credits
This software is a rewrite of [balatro-apk-maker](https://github.com/blake502/balatro-apk-maker). It uses [APKEditor](https://github.com/REAndroid/APKEditor) [Uber Apk Signer](https://github.com/patrickfav/uber-apk-signer) and [Love Android](https://github.com/love2d/love-android)