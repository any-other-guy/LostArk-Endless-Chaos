# Endless-Chaos

A Lost Ark chaos dungeon(PvE) farming bot.\
Fully automatic mob/elite/boss detecting and clearing, based on image recognition.\
Background running is capable and tested, by using Remote Desktop (RDP Wrapper) and Nvidia GeForce Now.\
UPDATE: Major improvements on efficiency and accuracy updated!! (12/14/2022 right before brel update in the west) Please re-install and go through all config files again.

What it does:
* Infinite Chaos Dungeon clears for any selected character
* Daily x2 Chaos Dungeon FULL runs. Able to rotate through UP to 9 characters, then switch back to your main character for more infinite run cycles.
* Daily Lopang runs on selected/all characters
* Daily Guild Donations on selected/all characters
* Daily Rapport Tasks on selected/all characters

Basic Features:
- [x] Floor 1 clearing
- [x] Floor 2 clearing
- [x] Gold Portal clearing
- [x] Purple Boss Portal clearing
- [x] Auto game restart on EAC offline or crash, for Steam and/or Nvidia GeForce Now players
- [x] Daily Lopang (extra setup required, pls refer to the pinned post in Issues)
- [x] Daily Guild Donation and research support
- [x] Daily Rapport Task on selected NPC

Utilities:
- [x] Auto repair
- [x] Auto health pot at low hp, customizable percentage
- [x] Anti-timeout detection
- [ ] A Lot More...

## Getting started (Please read)

### 0. Prerequisites:
- Install/Open a Command Line/Terminal app in your operating system.
- Install Python3 (if you dont have)
- Install pip (if you dont have) from your terminal:
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
python3 -m pip install --upgrade pip
```

### 1. Please change game settings to EXACTLY these numbers:

desktop resolution: 1920x1080\
In-game Video settings:
- Resolution: 1920x1080
- Screen: Borderless
- Force 21:9 Aspect Ratio checked

In-game Gameplay -> Controls and Display -> HUD size: 110%\
minimap transparency (at top right corner): 100%\
minimap zoom-in (at top right corner): 65%\
\
Please change game settings to EXACTLY these ^^ numbers

### 2. Configure character ability settings in ./config.py and ./abilities.py
IMPORTANT: \
please carefully setup paramters in ./config.py and ./abilities.py
refering to the comments for now.\
lots of things can be customized for your best experience.

### 3. Start running script:

```
git clone https://github.com/any-other-guy/Endless-Chaos.git
cd Endless-Chaos
pip install -r requirements.txt
python3 .\bot.py
```

\
Open a Github Issue if you need any assistance or have any feedback, appreciated!

## DISCLAIMER (VERY IMPORTANT): 
This script was created solely for fulfilling my personal learning purposes. I do not commercialize it in any way. If anything is against ToS, I would take it down from the public domain.
By running the script, you agree to accept any consequence at your own risk!
