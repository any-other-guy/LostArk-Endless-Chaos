# Endless-Chaos
Lost Ark chaos dungeon farming bot\
Fully automatic mob/elite/boss detecting and clearing\
Background running is supported with RDP Wrapper

Features:
- [x] Floor 1 clear
- [x] Floor 2 clear
- [x] Gold Portal
- [ ] Red Boss Portal
- [ ] Floor 3 clear

Utilities:
- [x] Auto repair
- [x] Auto health pot at low hp
- [x] Anti-stuck detection and time limit customization
- [ ] todo

## Getting started

###0. Prequisites
Install pip if you have not:
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
python3 -m pip install --upgrade pip
```


### 1.Please change game settings to: 
resolution: 1920x1080 borderless window, force 21:9 aspect ratio\
HUD size: 110%\
minimap transparency: 100%\
desktop resolution: 1920x1080

### 2.Configure character ability settings in /config.py

### 3.Start running script:
```
cd Endless-Chaos
pip install -r requirements.txt
python3 bot.py
```

IMPORTANT: by running the script, you agree to use it at your own risk!

