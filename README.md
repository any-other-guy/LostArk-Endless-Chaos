# Endless-Chaos

A Lost Ark chaos dungeon(PvE) farming bot.\
Fully automatic mob/elite/boss detecting and clearing, based on image recognition.\
Background running is supported with RDP Wrapper(Remote Desktop).

I have been mostly running the script for my rather buffed Sorceress, of course skill/engraving and etc are fine tuned both inside [config.py](config.py)
 and in-game. You will have to tune it yourself in order to run it smoothly and efficiently without the need of HP potion.\
So far my average 1445 dungeon floor1+2 run time is about 120-130 seconds, including loading time and random golden/purple portal appearances. A 1475 dungeon full clear is about 240-250 seconds per run. I might release a demo video in the near future...

Features:

- [x] Floor 1 clearing
- [x] Floor 2 clearing
- [x] Gold Portal clearing
- [x] Purple Boss Portal clearing
- [x] Optional Floor 3 daily clearing only
- [x] Optional Floor 3 indefinite clearing for silver earning
- [x] Auto spell cooldown detecting and cycling
- [x] Auto game client restart on game crash/disconnect issue (experimental)


Utilities:

- [x] Auto repair
- [x] Auto health pot at low hp, customizable percentage
- [x] Anti-timeout detection
- [x] Restart game client and continue running after EAC offline or game crash
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
todo.\
Default gameplay settings:
```
    "interact": "g",
    "move": "left",
    "blink": "space",
    "meleeAttack": "c",
    "awakening": "v",
    "healthPot": "f1",
    "healthPotAtPercent": 0.3,
    "selectLevel": True,
    "floor3": False,
    "autoRepair": True,
    "shortcutEnterChaos": True,
    "useHealthPot": True,
```


### 3.Start running script:

```
git clone https://github.com/any-other-guy/Endless-Chaos.git
cd Endless-Chaos
pip install -r requirements.txt
python3 .\bot.py
```

## VERY IMPORTANT: 
This script was created solely for fulfilling my personal learning purposes. I do not commercialize it in any way. If anything is against ToS, I would take it down from the public domain.
By running the script, you agree to accept any consequence at your own risk!
