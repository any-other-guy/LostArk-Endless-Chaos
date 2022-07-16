# Endless-Chaos

A Lost Ark chaos dungeon(PvE) farming bot.\
Fully automatic mob/elite/boss detecting and clearing, based on image recognition.\
Background running is supported with RDP Wrapper(Remote Desktop).

Features:

- [x] Floor 1 clearing
- [x] Floor 2 clearing
- [x] Gold Portal clearing
- [x] Purple Boss Portal clearing
- [x] Optional Floor 3 daily clearing only
- [x] Optional Floor 3 indefinite clearing for silver earning
- [x] Auto spell cooldown detecting and cycling


Utilities:

- [x] Auto repair
- [x] Auto health pot at low hp, customizable percentage
- [x] Anti-timeout detection
- [ ] More...

## Getting started

### 0. Prerequisites:
Install pip:

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
python3 -m pip install --upgrade pip
```

### 1.Please change game settings to exactly these numbers:

desktop resolution: 1920x1080\
game resolution: 1920x1080 borderless window, force 21:9 aspect ratio\
HUD size: 110%\
minimap transparency: 100%\
minimap zoom-in: 65%

### 2.Configure character ability settings in /config.py
lots of things can be customized for the best auto clearing experience\
todo..

### 3.Start running script:

```
git clone https://github.com/any-other-guy/Endless-Chaos.git
cd Endless-Chaos
pip install -r requirements.txt
python3 /bot.py
```

VERY IMPORTANT: 
This script was created solely for fulfilling my personal learning purposes. I do not commercialize it in any way. If anything is against ToS, I would take it down from the public domain.
By running the script, you agree to accept any consequence at your own risk!
