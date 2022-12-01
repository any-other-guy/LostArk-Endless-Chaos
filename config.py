"""
    IMPORTANT #1:
    Please change game settings to EXACTLY these numbers:
    desktop resolution: 1920x1080
    In-game Video settings:

    Resolution: 1920x1080
    Screen: Borderless
    Force 21:9 Aspect Ratio checked
    In-game Gameplay -> Controls and Display -> HUD size: 110%
    minimap transparency (at top right corner): 100%
    minimap zoom-in (at top right corner): 65%

    IMPORTANT #2: 
    config must be set up correctly in order for the bot to work properly on your machine.
    Refer to the inline comments below:

    For Lopang enjoyers:
    Set your first bifrost point to be at lopang island.
    Exact location to be right in front of the NPC machine which stands farthest to the entrance.
    Then set your 2/4/5 (because i dont have no3 unlocked) bifrost location to be right in front of those three lopang quest hand-in NPCs.
"""
config = {
    "mainCharacter": 0,  # must be in number 0 to 5 (0 is the first character)
    "enableLopang": True,  # NOTE: you need to setup bifrost locations properly for this, at very specific locations. Look up ^
    "enableGuildDonation": True,  # please make sure all your characters have a guild
    # Setup your characters below:
    # can setup UP TO 9 characters for daily chaos/lopang/guild stuff
    # however your main must be in character 0 to 5 (just for re-connect back after disconnection happens)
    # ilvl-endless is the dungeon which you want to run infinitely
    # ilvl-aor is the daily aura of resonance dungeon you only want to run TWICE per day
    # IMPORTANT: dungeon ilvl choices are only limited to 1475, 1445, 1370, 1110 for now. I will add more later when brel comes out
    "characters": [
        {
            "index": 0,
            "class": "sorceress",
            "ilvl-endless": 1475,
            "ilvl-aor": 1475,
            "lopang": False,
            "guildDonation": True,
        },
        {
            "index": 1,
            "class": "arcana",
            "ilvl-endless": 1370,
            "ilvl-aor": 1475,
            "lopang": False,
            "guildDonation": True,
        },
        {
            "index": 2,
            "class": "sorceress",
            "ilvl-endless": 1370,
            "ilvl-aor": 1445,
            "lopang": True,
            "guildDonation": True,
        },
        {
            "index": 3,
            "class": "sorceress",
            "ilvl-endless": 1370,
            "ilvl-aor": 1370,
            "lopang": True,
            "guildDonation": True,
        },
        {
            "index": 4,
            "class": "sorceress",
            "ilvl-endless": 1370,
            "ilvl-aor": 1370,
            "lopang": True,
            "guildDonation": True,
        },
        {
            "index": 5,
            "class": "sorceress",
            "ilvl-endless": 1370,
            "ilvl-aor": 1370,
            "lopang": True,
            "guildDonation": True,
        },
        {
            "index": 6,
            "class": "deathblade",
            "ilvl-endless": 1100,
            "ilvl-aor": 1100,
            "lopang": True,
            "guildDonation": True,
        },
    ],
    "floor3Mode": False,  # only enable if you ONLY want to run infinite floor3 clearing
    "selectLevel": True,  # TODO: to be deprecated soon, DO NOT TOUCH
    "performance": False,  # set True for lower-end PCs
    "interact": "g",  # change this if you have binded it to something else eg.mouse button
    "move": "left",  # or "right"
    "blink": "space",
    "meleeAttack": "c",
    "awakening": "v",
    "healthPot": "f1",  # important to put your regen potion on this button
    "healthPotAtPercent": 0.3,  # health threshold to trigger potion
    # "useAwakening": True, # not checking this for now
    # "useSpeciality1": True, # not checking this for now
    # "useSpeciality2": True, # not checking this for now
    "auraRepair": True,  # True if you have aura, if not then for non-aura users: MUST have your character parked near a repairer in city before starting the script
    "shortcutEnterChaos": True,  # you want to use True
    "useHealthPot": True,  # you want to use True
    # You might not want to touch anything below, because I assume you have your game setup same as mine :) otherwise something might not work properly!
    "regions": {
        "minimap": (1655, 170, 260, 200),  # (1700, 200, 125, 120)
        "abilities": (625, 779, 300, 155),
        "leaveMenu": (0, 154, 250, 300),
        "buffs": (625, 779, 300, 60),
        "center": (782, 353, 400, 350),
    },
    "screenResolutionX": 1920,
    "screenResolutionY": 1080,
    "clickableAreaX": 500,
    "clickableAreaY": 250,
    "screenCenterX": 960,
    "screenCenterY": 540,
    "minimapCenterX": 1772,
    "minimapCenterY": 272,
    "timeLimit": 420000,  # to prevent unexpected amount of time spent in a chaos dungeon, a tiem limit is set here, will quit after this amount of seconds
    "blackScreenTimeLimit": 30000,  # if stuck in nothing for this amount of time, alt f4 game, restart and resume.
    "delayedStart": 3300,
    "healthCheckX": 690,
    "healthCheckY": 854,
    "charSwitchX": 540,
    "charSwitchY": 683,
    "charPositionsAtCharSelect": [
        [500, 827],
        [681, 827],
        [874, 827],
        [1050, 827],
        [1237, 827],
        [1425, 827],
    ],
    "charPositions": [
        [760, 440],
        [960, 440],
        [1160, 440],
        [760, 530],
        [960, 530],
        [1160, 530],
        [760, 620],
        [960, 620],
        [1160, 620],
    ],
    "charSelectConnectX": 1030,
    "charSelectConnectY": 684,
    "charSelectOkX": 920,
    "charSelectOkY": 590,
}
