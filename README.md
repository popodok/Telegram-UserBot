![logo](https://telegra.ph/file/73cf4c62b2c64f981961e.png)
# Telegram-UserBot

Originaly developed by RaphielGang. Forked and modificated by me. Also there are some modules from [PaperplaneExtended](https://github.com/AvinashReddy3108/PaperplaneExtended) and [Friendly Telegram](https://gitlab.com/friendly-telegram)


### If you find any bugs or have any suggestions then don't hesitate to contact me in [telegram](https://t.me/Polisan_The_Easy_Nick).

### How to run it locally on linux device:
- install python 3.7
Ubuntu Based:
```
$ sudo apt install python3.7 ffmpeg libopus-dev python-pip3 poppler-utils libpq-dev redis-server cairosvg
```
Debian Based:
```
$ sudo apt update
$ sudo apt install build-essential ffmpeg libopus-dev zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev
$ curl -O https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tar.xz
$ tar -xf Python-3.7.9.tar.xz
$ cd Python-3.7.9.tar.xz
$ ./configure --enable-optimizations
$ make -j *number of kernels*
$ sudo make altinstall
```
Alpine Linux:
```
$ apk add python3
```
Arch Linux:
```
$ sudo pacman -S python
```
 
- type: 
```
git clone https://github.com/popodok/Telegram-UserBot.git
cd Telegram-UserBot
python3.7 -m pip install -r requirements.txt
```
- fill config.env with nano, vim etc
- run ./init/start.py

### How to run it on Docker:
```
git clone https://github.com/popodok/Telegram-UserBot.git
cd Telegram-UserBot
```
- fill config.env with nano, vim etc
- install Docker
- type:
```
# docker build . -t bot 
# docker run bot
```
### How to run it on termux:
```
pkg update
pkg install git
git clone https://github.com/popodok/Telegram-UserBot.git
cd Telegram-UserBot
```
- fill config.env with nano, vim etc
- run ./termux_installer.sh
- run ./init/start.py

### Deploy on Heroku:
<p align="left"><a href="https://heroku.com/deploy"> <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy to Heroku" /></a></p>

### If the CI builds pass, but you still get syntax errors when running locally it's most probably not a problem with the source but with your version of python



```
#include <std/disclaimer.h>
/**
    Your Telegram account may get banned.
    I am not responsible for any improper use of this bot
    This bot is intended for the purpose of having fun with memes,
    as well as efficiently managing groups.
    You ended up spamming groups, getting reported left and right,
    and you ended up in a Finale Battle with Telegram and at the end
    Telegram Team deleted your account?
    And after that, then you pointed your fingers at us
    for getting your acoount deleted?
    I will rolling on the floor laughing at you.
/**
```

A modular telegram Python UserBot running on python3 with a mongoDB coupled with Redis backend.

Started up as a simple bot, which helps with deleting messages and other stuffs when I didn't possess a smartphone(selecting each message indeed difficult) with a ton of meme features kanged from [SkittBot](https://github.com/skittles9823/SkittBot), it has evolved, becoming extremely modular and simple to use.

For configuring this userbot, you can checkout the [Wiki](https://wiki.raphielgang.org)

If you just want to stay in the loop about new features or
announcements you can join the [news channel](https://t.me/maestro_userbot_channel).



Please head to the wiki on instructions to setting it up!


### Contributing to the source:

We love to see you contributing and helping us improve on our way to a perfect userbot.

If you need help writing a new module, you can checkout the [Wiki](https://wiki.raphielgang.org).

Please target your PRs to the staging branch and not master. Commits on `master` wont be done by a user.


### Credits:

I would like to thank people who assisted me throughout this project:

* [@YouTwitFace](https://github.com/YouTwitFace)
* [@TheDevXen](https://github.com/TheDevXen)
* [@Skittles9823](https://github.com/Skittles9823)
* [@deletescape](https://github.com/deletescape)
* [@songotenks69](https://github.com/songotenks69)
* [@Ovenoboyo](https://github.com/Ovenoboyo)
* [SphericalKat](https://github.com/ATechnoHazard)
* [@rupansh](https://github.com/rupansh)
* [@zakaryan2004](https://github.com/zakaryan2004)
* [@kandnub](https://github.com/kandnub)
* [@pqhaz](https://github.com/pqhaz)
* [@yshalsager](https://github.com/yshalsager)

and many more people who aren't mentioned here.

Found Bugs? Create an issue on the issue tracker, or post it in the [support group](https://t.me/userbot_support).
