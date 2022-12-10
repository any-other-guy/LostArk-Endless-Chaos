from config import config
from abilities import abilities
import pyautogui
import pydirectinput
import time
import random
import math
import argparse

newStates = {
    "status": "inCity",
    "abilities": [],
    "abilityScreenshots": [],
    "clearCount": 0,
    "fullClearCount": 0,
    "moveToX": config["screenCenterX"],
    "moveToY": config["screenCenterY"],
    "moveTime": 0,
    "botStartTime": None,
    "instanceStartTime": None,
    "deathCount": 0,
    "healthPotCount": 0,
    "timeoutCount": 0,
    "goldPortalCount": 0,
    "purplePortalCount": 0,
    "badRunCount": 0,
    "gameRestartCount": 0,
    "gameCrashCount": 0,
    "gameOfflineCount": 0,
    "minTime": config["timeLimit"],
    "maxTime": -1,
    "floor3Mode": False,
    "multiCharacterMode": False,
    "currentCharacter": config["mainCharacter"],
    "multiCharacterModeState": [],
}


def main():
    print("Endless Chaos starting in seconds...")
    print("Remember to turn on Auto-disassemble")

    # Instantiate the parser
    parser = argparse.ArgumentParser(description="Optional app description")
    parser.add_argument("--lunshua", action="store_true", help="A boolean switch")
    parser.add_argument("--buy", action="store_true", help="A boolean switch")
    args = parser.parse_args()

    if args.lunshua:
        states["multiCharacterMode"] = True
        for i in range(len(config["characters"])):
            states["multiCharacterModeState"].append(2)
        print(
            "lunshua start, running full runs on characters: {}".format(
                states["multiCharacterModeState"]
            )
        )

    if args.buy:
        buyAuctionFirstFav()

    sleep(3000, 3300)
    meleeClick = "right"
    if config["move"] == "right":
        meleeClick = "left"
    pydirectinput.moveTo(x=config["screenCenterX"], y=config["screenCenterY"])
    sleep(200, 300)
    pydirectinput.click(button=meleeClick)
    sleep(300, 400)

    # forceing no floor3 full clear with performance mode
    if config["performance"] == True:
        states["floor3Mode"] = False

    # save bot start time
    states["botStartTime"] = int(time.time_ns() / 1000000)

    while True:
        if states["status"] == "inCity":
            # initialize new states
            states["abilityScreenshots"] = []

            sleep(1000, 1200)
            if offlineCheck():
                closeGameByClickingDialogue()
                continue
            if gameCrashCheck():
                states["status"] = "restart"
                continue

            # wait until loaded
            while True:
                if gameCrashCheck():
                    states["status"] = "restart"
                    break
                if offlineCheck():
                    closeGameByClickingDialogue()
                    break
                sleep(1000, 1200)
                inTown = pyautogui.locateCenterOnScreen(
                    "./screenshots/inTown.png",
                    confidence=0.75,
                    region=(1870, 133, 25, 30),
                )
                inChaos = pyautogui.locateCenterOnScreen(
                    "./screenshots/inChaos.png",
                    confidence=0.75,
                    region=(247, 146, 222, 50),
                )
                if inChaos != None:
                    print("still in the last chaos run, quitting")
                    quitChaos()
                    sleep(4000, 6000)
                if inTown != None:
                    print("city loaded")
                    break
                sleep(1400, 1600)

            pydirectinput.moveTo(x=config["screenCenterX"], y=config["screenCenterY"])
            sleep(100, 200)

            if offlineCheck():
                closeGameByClickingDialogue()
                continue
            if gameCrashCheck():
                states["status"] = "restart"
                continue
            # for non-aura users: MUST have your character parked near a repairer in city before starting the script
            if config["auraRepair"] == False:
                doCityRepair()

            # switch character
            if states["multiCharacterMode"]:
                if sum(states["multiCharacterModeState"]) == 0:
                    # repair
                    if config["auraRepair"]:
                        doAuraRepair(True)
                    sleep(1400, 1600)
                    # guild dono
                    if (
                        config["enableGuildDonation"]
                        and config["characters"][states["currentCharacter"]][
                            "guildDonation"
                        ]
                    ):
                        sleep(1400, 1600)
                        doGuildDonation()
                        sleep(1400, 1600)
                    # rapport
                    if (
                        config["enableRapport"]
                        and config["characters"][states["currentCharacter"]]["rapport"]
                    ):
                        sleep(500, 1000)
                        print("Doing Rapport")
                        doRapport()
                        sleep(1400, 1600)
                    if gameCrashCheck():
                        states["status"] = "restart"
                        continue
                    if offlineCheck():
                        closeGameByClickingDialogue()
                        continue

                    # lopang
                    if (
                        config["enableLopang"]
                        and config["characters"][states["currentCharacter"]]["lopang"]
                    ):
                        # do lopang
                        print("doing lopang on : {}".format(states["currentCharacter"]))
                        doLopang()
                        sleep(1400, 1600)

                    if gameCrashCheck():
                        states["status"] = "restart"
                        continue
                    if offlineCheck():
                        closeGameByClickingDialogue()
                        continue

                    # just finished last char before main
                    print(
                        "just finished last char before main, closing multi-char mode"
                    )
                    states["multiCharacterMode"] = False
                    states["multiCharacterModeState"] = []
                    switchToCharacter(config["mainCharacter"])
                    continue
                elif states["multiCharacterModeState"][states["currentCharacter"]] <= 0:
                    # repair
                    if config["auraRepair"]:
                        doAuraRepair(True)
                    sleep(1400, 1600)
                    # guild dono
                    if (
                        config["enableGuildDonation"]
                        and config["characters"][states["currentCharacter"]][
                            "guildDonation"
                        ]
                    ):
                        sleep(1400, 1600)
                        doGuildDonation()
                        sleep(1400, 1600)
                    # rapport
                    if (
                        config["enableRapport"]
                        and config["characters"][states["currentCharacter"]]["rapport"]
                    ):
                        sleep(500, 1000)
                        print("Doing Rapport")
                        doRapport()
                        sleep(1400, 1600)
                    if gameCrashCheck():
                        states["status"] = "restart"
                        continue
                    if offlineCheck():
                        closeGameByClickingDialogue()
                        continue

                    # lopang
                    sleep(1400, 1600)
                    if (
                        config["enableLopang"]
                        and config["characters"][states["currentCharacter"]]["lopang"]
                    ):
                        # do lopang
                        print("doing lopang on : {}".format(states["currentCharacter"]))
                        doLopang()
                        sleep(1400, 1600)

                    if gameCrashCheck():
                        states["status"] = "restart"
                        continue
                    if offlineCheck():
                        closeGameByClickingDialogue()
                        continue
                    # switch to next
                    nextIndex = (states["currentCharacter"] + 1) % len(
                        states["multiCharacterModeState"]
                    )
                    print(
                        "character: {} 's daily x2 is done, switching to next: {}".format(
                            states["currentCharacter"], nextIndex
                        )
                    )
                    switchToCharacter(nextIndex)
                    continue

            states["floor3Mode"] = False
            # only do floor3 if user has set to do, and when aor/multi-char is presented
            if config["floor3Mode"] == True or states["multiCharacterMode"]:
                states["floor3Mode"] = True

            sleep(500, 600)
            # clearQuest()
            enterChaos()

            # save instance start time
            states["instanceStartTime"] = int(time.time_ns() / 1000000)
            if gameCrashCheck():
                states["status"] = "restart"
                continue
            if offlineCheck():
                closeGameByClickingDialogue()
                continue

        elif states["status"] == "floor1":
            print("floor1")
            sleep(1000, 1300)
            # wait for loading
            waitForLoading()
            pydirectinput.moveTo(x=config["screenCenterX"], y=config["screenCenterY"])
            sleep(100, 200)
            if gameCrashCheck():
                states["status"] = "restart"
                continue
            if offlineCheck():
                closeGameByClickingDialogue()
                continue
            if checkTimeout():
                quitChaos()
                continue
            sleep(1000, 1200)
            print("floor1 loaded")

            # saving clean abilities icons

            saveAbilitiesScreenshots()

            # do floor one
            doFloor1()
        elif states["status"] == "floor2":
            print("floor2")
            sleep(1000, 1300)
            # wait for loading
            waitForLoading()
            pydirectinput.moveTo(x=config["screenCenterX"], y=config["screenCenterY"])
            sleep(100, 200)
            if gameCrashCheck():
                states["status"] = "restart"
                continue
            if offlineCheck():
                closeGameByClickingDialogue()
                continue
            if checkTimeout():
                quitChaos()
                continue
            print("floor2 loaded")
            # do floor two
            doFloor2()
        elif states["status"] == "floor3":
            print("floor3")
            sleep(1000, 1300)
            # wait for loading
            waitForLoading()
            pydirectinput.moveTo(x=config["screenCenterX"], y=config["screenCenterY"])
            sleep(100, 200)
            if gameCrashCheck():
                states["status"] = "restart"
                continue
            if offlineCheck():
                closeGameByClickingDialogue()
                continue
            if checkTimeout():
                quitChaos()
                continue
            print("floor3 loaded")
            # do floor 3
            # trigger start floor 3
            pydirectinput.moveTo(x=760, y=750)
            sleep(100, 120)
            pydirectinput.click(button=config["move"])
            sleep(200, 300)
            pydirectinput.click(button=config["move"])
            sleep(200, 300)
            doFloor3Portal()
            if checkTimeout() or states["floor3Mode"] == False:
                if gameCrashCheck():
                    states["status"] = "restart"
                    continue
                if offlineCheck():
                    closeGameByClickingDialogue()
                    continue
                quitChaos()
                continue
            doFloor3()
        elif states["status"] == "restart":
            sleep(10000, 12200)
            restartGame()
            while True:
                im = pyautogui.screenshot(region=(1652, 168, 240, 210))
                r, g, b = im.getpixel((1772 - 1652, 272 - 168))
                if r + g + b > 10:
                    print("game restarted")
                    break
                sleep(200, 300)
            sleep(600, 800)
            inChaos = pyautogui.locateCenterOnScreen(
                "./screenshots/inChaos.png", confidence=0.75, region=(247, 146, 222, 50)
            )
            if inChaos != None:
                print("still in the last chaos run, quitting")
                quitChaos()
            else:
                print("in city, going for next run")
                states["status"] = "inCity"


def enterChaos():
    blackScreenStartTime = int(time.time_ns() / 1000000)
    if config["shortcutEnterChaos"] == True:
        # wait for last run black screen
        while True:
            im = pyautogui.screenshot(region=(1652, 168, 240, 210))
            r, g, b = im.getpixel((1772 - 1652, 272 - 168))
            if r + g + b > 10:
                break
            sleep(200, 300)

            currentTime = int(time.time_ns() / 1000000)
            if currentTime - blackScreenStartTime > config["blackScreenTimeLimit"]:
                pydirectinput.keyDown("alt")
                sleep(350, 400)
                pydirectinput.keyDown("f4")
                sleep(350, 400)
                pydirectinput.keyUp("alt")
                sleep(350, 400)
                pydirectinput.keyUp("f4")
                sleep(350, 400)
                sleep(10000, 15000)
                return
        sleep(600, 800)
        while True:
            if gameCrashCheck():
                return
            if offlineCheck():
                closeGameByClickingDialogue()
                return
            pydirectinput.keyDown("alt")
            sleep(100, 200)
            pydirectinput.press("q")
            sleep(100, 200)
            pydirectinput.keyUp("alt")
            sleep(1000, 1200)

            aor = pyautogui.locateCenterOnScreen(
                "./screenshots/aor.png", confidence=0.8, region=(592, 304, 192, 95)
            )
            if aor != None and config["performance"] == False:
                states["floor3Mode"] = True
                print("aor detected")
                if (
                    config["enableMultiCharacterMode"] == True
                    and states["currentCharacter"] == config["mainCharacter"]
                    and states["multiCharacterMode"] == False
                ):
                    states["multiCharacterMode"] = True
                    for i in range(len(config["characters"])):
                        states["multiCharacterModeState"].append(2)
                    print(
                        "aura of resonance detected, running full runs on characters: {}".format(
                            states["multiCharacterModeState"]
                        )
                    )
            pydirectinput.moveTo(886, 346)
            sleep(500, 600)
            pydirectinput.click(button="left")
            sleep(500, 600)
            pydirectinput.moveTo(886, 346)
            sleep(500, 600)
            pydirectinput.click(button="left")
            sleep(500, 600)

            # select chaos dungeon level based on states
            _curr = config["characters"][states["currentCharacter"]]
            if states["multiCharacterMode"] or aor != None:
                if _curr["ilvl-aor"] == 1100:
                    # punica
                    pydirectinput.moveTo(1112, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # star 1
                    pydirectinput.moveTo(524, 398)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                elif _curr["ilvl-aor"] == 1310:
                    # punica
                    pydirectinput.moveTo(1112, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # star 2
                    pydirectinput.moveTo(524, 455)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                elif _curr["ilvl-aor"] == 1325:
                    # punica
                    pydirectinput.moveTo(1112, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # moon 1
                    pydirectinput.moveTo(524, 505)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                elif _curr["ilvl-aor"] == 1340:
                    # punica
                    pydirectinput.moveTo(1112, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # moon 2
                    pydirectinput.moveTo(524, 555)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                elif _curr["ilvl-aor"] == 1355:
                    # punica
                    pydirectinput.moveTo(1112, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # moon 2
                    pydirectinput.moveTo(524, 605)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                elif _curr["ilvl-aor"] == 1370:
                    # punica
                    pydirectinput.moveTo(1112, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # sun 1
                    pydirectinput.moveTo(524, 662)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                elif _curr["ilvl-aor"] == 1385:
                    # punica
                    pydirectinput.moveTo(1112, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # sun 2
                    pydirectinput.moveTo(524, 715)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                elif _curr["ilvl-aor"] == 1400:
                    # punica
                    pydirectinput.moveTo(1112, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # sun 3
                    pydirectinput.moveTo(524, 770)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                elif _curr["ilvl-aor"] == 1415:
                    # south vern
                    pydirectinput.moveTo(1266, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # corruption 1
                    pydirectinput.moveTo(524, 400)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                elif _curr["ilvl-aor"] == 1445:
                    # south vern
                    pydirectinput.moveTo(1266, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # corruption 2
                    pydirectinput.moveTo(524, 451)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                elif _curr["ilvl-aor"] == 1475:
                    # south vern
                    pydirectinput.moveTo(1266, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # corruption 3
                    pydirectinput.moveTo(524, 504)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
            else:
                if _curr["ilvl-endless"] == 1100:
                    # punica
                    pydirectinput.moveTo(1112, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # star 1
                    pydirectinput.moveTo(524, 398)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                elif _curr["ilvl-endless"] == 1310:
                    # punica
                    pydirectinput.moveTo(1112, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # star 2
                    pydirectinput.moveTo(524, 455)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                elif _curr["ilvl-endless"] == 1325:
                    # punica
                    pydirectinput.moveTo(1112, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # moon 1
                    pydirectinput.moveTo(524, 505)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                elif _curr["ilvl-endless"] == 1340:
                    # punica
                    pydirectinput.moveTo(1112, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # moon 2
                    pydirectinput.moveTo(524, 555)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                elif _curr["ilvl-endless"] == 1355:
                    # punica
                    pydirectinput.moveTo(1112, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # moon 2
                    pydirectinput.moveTo(524, 605)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                elif _curr["ilvl-endless"] == 1370:
                    # punica
                    pydirectinput.moveTo(1112, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # sun 1
                    pydirectinput.moveTo(524, 662)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                elif _curr["ilvl-endless"] == 1385:
                    # punica
                    pydirectinput.moveTo(1112, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # sun 2
                    pydirectinput.moveTo(524, 715)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                elif _curr["ilvl-endless"] == 1400:
                    # punica
                    pydirectinput.moveTo(1112, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # sun 3
                    pydirectinput.moveTo(524, 770)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                elif _curr["ilvl-endless"] == 1415:
                    # south vern
                    pydirectinput.moveTo(1266, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # corruption 1
                    pydirectinput.moveTo(524, 400)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                elif _curr["ilvl-endless"] == 1445:
                    # south vern
                    pydirectinput.moveTo(1266, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # corruption 2
                    pydirectinput.moveTo(524, 451)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                elif _curr["ilvl-endless"] == 1475:
                    # south vern
                    pydirectinput.moveTo(1266, 307)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)
                    # corruption 3
                    pydirectinput.moveTo(524, 504)
                    sleep(500, 600)
                    pydirectinput.click(button="left")
                    sleep(500, 600)

            enterButton = pyautogui.locateCenterOnScreen(
                "./screenshots/enterButton.png",
                confidence=0.75,
                region=(1334, 754, 120, 60),
            )
            if enterButton != None:
                x, y = enterButton
                pydirectinput.moveTo(x=x, y=y)
                sleep(200, 300)
                pydirectinput.click(x=x, y=y, button="left")
                sleep(100, 200)
                pydirectinput.click(x=x, y=y, button="left")
                sleep(100, 200)
                pydirectinput.click(x=x, y=y, button="left")
                break
            else:
                pydirectinput.moveTo(886, 346)
                sleep(200, 300)
                pydirectinput.click(button="left")
                sleep(200, 300)
    else:
        while True:
            if gameCrashCheck():
                return
            if offlineCheck():
                closeGameByClickingDialogue()
                return
            enterHand = pyautogui.locateOnScreen(
                "./screenshots/enterChaos.png", confidence=config["confidenceForGFN"]
            )
            if enterHand != None:
                print("entering chaos...")
                pydirectinput.press(config["interact"])
                break
            sleep(200, 300)
    sleep(500, 600)
    while True:
        if gameCrashCheck():
            return
        # if offlineCheck():
        #     closeGameByClickingDialogue()
        #     return
        dc = pyautogui.locateOnScreen(
            "./screenshots/dc.png",
            region=config["regions"]["center"],
            confidence=config["confidenceForGFN"],
        )
        enterServer = pyautogui.locateCenterOnScreen(
            "./screenshots/enterServer.png", confidence=0.98, region=(885, 801, 160, 55)
        )
        if dc != None or enterServer != None:
            closeGameByClickingDialogue()
            return

        acceptButton = pyautogui.locateCenterOnScreen(
            "./screenshots/acceptButton.png",
            confidence=0.75,
            region=config["regions"]["center"],
        )
        if acceptButton != None:
            x, y = acceptButton
            pydirectinput.moveTo(x=x, y=y)
            sleep(200, 300)
            pydirectinput.click(x=x, y=y, button="left")
            sleep(100, 200)
            pydirectinput.click(x=x, y=y, button="left")
            sleep(100, 200)
            pydirectinput.click(x=x, y=y, button="left")
            break
        sleep(500, 600)
    states["status"] = "floor1"
    return


def doFloor1():
    clearQuest()
    sleep(500, 550)
    # check repair
    if config["auraRepair"]:
        doAuraRepair(False)
    # trigger start floor 1
    pydirectinput.moveTo(x=845, y=600)
    sleep(450, 500)
    pydirectinput.click(button=config["move"])

    # delayed start for better aoe abiltiy usage at floor1 beginning
    if config["delayedStart"] != None and config["performance"] == False:
        sleep(config["delayedStart"] - 100, config["delayedStart"] + 100)

    if offlineCheck():
        closeGameByClickingDialogue()
        return
    if gameCrashCheck():
        states["status"] = "restart"
        return
    # # move to a side
    # pydirectinput.press(config["blink"])
    # sleep(400, 500)

    # pydirectinput.click(random.randint(800, 1120), random.randint(540, 580), button=config['move'])
    # sleep(2000,2200)
    # pydirectinput.click(x=960, y=530, button=config['move'])

    # # test
    # if config["performance"] == True:
    #     pydirectinput.press(config["awakening"])

    while True:
        # smash available abilities
        useAbilities()

        if offlineCheck():
            closeGameByClickingDialogue()
            return
        if gameCrashCheck():
            states["status"] = "restart"
            return
        if checkTimeout():
            quitChaos()
            return

        print("floor 1 cleared")
        calculateMinimapRelative(states["moveToX"], states["moveToY"])
        if enterPortal():
            break

    if offlineCheck():
        closeGameByClickingDialogue()
        return
    if gameCrashCheck():
        states["status"] = "restart"
        return
    if checkTimeout():
        quitChaos()
        return
    states["status"] = "floor2"
    return


def doFloor2():
    clearQuest()
    sleep(500, 550)
    # check repair
    if config["auraRepair"]:
        doAuraRepair(False)
    # trigger start floor 2
    pydirectinput.click(x=1150, y=500, button=config["move"])
    sleep(800, 900)
    pydirectinput.click(x=960, y=200, button=config["move"])
    sleep(800, 900)
    pydirectinput.click(x=945, y=550, button=config["move"])

    while True:
        useAbilities()

        if offlineCheck():
            closeGameByClickingDialogue()
            return
        if gameCrashCheck():
            states["status"] = "restart"
            return
        if checkTimeout():
            quitChaos()
            return

        print("floor 2 cleared")
        if states["floor3Mode"] == False:
            states["clearCount"] = states["clearCount"] + 1
        calculateMinimapRelative(states["moveToX"], states["moveToY"])
        if enterPortal():
            break

    if offlineCheck():
        closeGameByClickingDialogue()
        return
    if gameCrashCheck():
        states["status"] = "restart"
        return
    if checkTimeout():
        quitChaos()
        return
    states["status"] = "floor3"
    return


def doFloor3Portal():
    bossBar = None
    goldMob = False
    normalMob = False
    for i in range(0, 10):
        goldMob = checkFloor3GoldMob()
        normalMob = checkFloor2Mob()
        bossBar = pyautogui.locateOnScreen(
            "./screenshots/bossBar.png", confidence=0.7, region=(406, 159, 1000, 200)
        )
        if normalMob == True:
            return
        if goldMob == True or bossBar != None:
            break
        sleep(500, 550)

    if goldMob == False and bossBar == None and states["floor3Mode"] == False:
        return

    if bossBar != None:
        print("purple boss bar located")
        states["purplePortalCount"] = states["purplePortalCount"] + 1
        pydirectinput.press(config["awakening"])
        while True:
            useAbilities()

            if offlineCheck():
                closeGameByClickingDialogue()
                return
            if gameCrashCheck():
                states["status"] = "restart"
                return
            if checkTimeout():
                # no quitChaos() here because it does it in upper function
                return

            print("special portal cleared")
            sleep(800, 900)
            if states["floor3Mode"] == False:
                return
            calculateMinimapRelative(states["moveToX"], states["moveToY"])

            if enterPortal():
                break
        sleep(800, 900)
    elif normalMob == True:
        return
    elif goldMob == True:
        print("gold mob located")
        states["goldPortalCount"] = states["goldPortalCount"] + 1
        while True:
            useAbilities()

            if offlineCheck():
                closeGameByClickingDialogue()
                return
            if gameCrashCheck():
                states["status"] = "restart"
                return
            if checkTimeout():
                # no quitChaos() here because it does it in upper function
                return

            print("special portal cleared")
            sleep(800, 900)
            if states["floor3Mode"] == False:
                return
            calculateMinimapRelative(states["moveToX"], states["moveToY"])
            if enterPortal():
                break
        sleep(800, 900)
    else:
        # hacky quit
        states["instanceStartTime"] = -1
        return

    if offlineCheck():
        closeGameByClickingDialogue()
        return
    if gameCrashCheck():
        states["status"] = "restart"
        return
    if checkTimeout():
        return


def doFloor3():
    waitForLoading()
    pydirectinput.moveTo(x=config["screenCenterX"], y=config["screenCenterY"])
    sleep(100, 200)
    if offlineCheck():
        closeGameByClickingDialogue()
        return
    if gameCrashCheck():
        states["status"] = "restart"
        return
    if checkTimeout():
        quitChaos()
        return

    print("real floor 3 loaded")

    clearQuest()
    sleep(500, 550)
    # check repair
    if config["auraRepair"]:
        doAuraRepair(False)
    # trigger start real floor 3
    useAbilities()

    if offlineCheck():
        closeGameByClickingDialogue()
        return
    if gameCrashCheck():
        states["status"] = "restart"
        return
    if checkTimeout():
        quitChaos()
        return

    print("Chaos Dungeon Full cleared")
    if config["floor3Mode"] == True:
        # restartChaos()
        quitChaos()  # to check aor, for multi-char mode
    else:
        quitChaos()
    return


def quitChaos():
    checkChaosFinish()
    # quit
    print("quitting chaos")
    sleep(100, 200)
    while True:
        leaveButton = pyautogui.locateCenterOnScreen(
            "./screenshots/leave.png",
            grayscale=True,
            confidence=0.7,
            region=config["regions"]["leaveMenu"],
        )

        if leaveButton != None:
            x, y = leaveButton

            # while (
            #     pyautogui.locateCenterOnScreen("./screenshots/ok.png", confidence=0.75)
            #     == None
            # ):
            pydirectinput.moveTo(x=x, y=y)
            sleep(200, 300)
            pydirectinput.click(button="left")
            sleep(100, 200)
        else:
            if offlineCheck():
                closeGameByClickingDialogue()
                return
            if gameCrashCheck():
                states["status"] = "restart"
                return
        sleep(300, 400)
        # leave ok
        okButton = pyautogui.locateCenterOnScreen(
            "./screenshots/ok.png",
            confidence=0.75,
            region=config["regions"]["center"],
        )
        if okButton != None:
            break
        sleep(300, 400)
    sleep(100, 200)
    checkChaosFinish()
    sleep(100, 200)
    while True:
        okButton = pyautogui.locateCenterOnScreen(
            "./screenshots/ok.png",
            confidence=0.75,
            region=config["regions"]["center"],
        )
        if okButton != None:
            x, y = okButton
            pydirectinput.moveTo(x=x, y=y)
            sleep(200, 300)
            pydirectinput.click(button="left")
            sleep(200, 300)
            pydirectinput.moveTo(x=x, y=y)
            sleep(100, 200)
            pydirectinput.click(button="left")
            sleep(100, 200)
            pydirectinput.moveTo(x=x, y=y)
            sleep(100, 200)
            pydirectinput.click(button="left")
            break
        sleep(300, 400)
    printResult()
    if states["multiCharacterMode"]:
        states["multiCharacterModeState"][states["currentCharacter"]] = (
            states["multiCharacterModeState"][states["currentCharacter"]] - 1
        )
        print(
            "currentCharacter: {}, multiCharacterModeState: {}".format(
                states["currentCharacter"], states["multiCharacterModeState"]
            )
        )
    states["status"] = "inCity"
    sleep(4000, 6000)
    return


# not using for now
def restartChaos():
    printResult()
    sleep(1200, 1400)
    # states["abilityScreenshots"] = []
    states["instanceStartTime"] = int(time.time_ns() / 1000000)

    while True:
        selectLevelButton = pyautogui.locateCenterOnScreen(
            "./screenshots/selectLevel.png",
            grayscale=True,
            confidence=0.7,
            region=config["regions"]["leaveMenu"],
        )
        if selectLevelButton != None:
            x, y = selectLevelButton

            pydirectinput.moveTo(x=x, y=y)
            sleep(200, 300)
            pydirectinput.click(button="left")
            sleep(100, 200)
            break
        sleep(100, 200)
    sleep(100, 200)
    while True:
        enterButton = pyautogui.locateCenterOnScreen(
            "./screenshots/enterButton.png",
            confidence=0.75,
            region=(1334, 754, 120, 60),
        )
        if enterButton != None:
            x, y = enterButton
            pydirectinput.moveTo(x=x, y=y)
            sleep(200, 300)
            pydirectinput.click(x=x, y=y, button="left")
            sleep(100, 200)
            pydirectinput.click(x=x, y=y, button="left")
            sleep(100, 200)
            pydirectinput.click(x=x, y=y, button="left")
            break
        sleep(100, 200)
    sleep(100, 200)
    while True:
        acceptButton = pyautogui.locateCenterOnScreen(
            "./screenshots/acceptButton.png",
            confidence=0.75,
            region=config["regions"]["center"],
        )
        if acceptButton != None:
            x, y = acceptButton
            pydirectinput.moveTo(x=x, y=y)
            sleep(200, 300)
            pydirectinput.click(x=x, y=y, button="left")
            sleep(100, 200)
            pydirectinput.click(x=x, y=y, button="left")
            sleep(100, 200)
            pydirectinput.click(x=x, y=y, button="left")
            break
        sleep(100, 200)
    states["status"] = "floor1"
    sleep(2000, 3200)
    return


def printResult():
    if int(states["clearCount"] + states["fullClearCount"]) == 0:
        return
    lastRun = (int(time.time_ns() / 1000000) - states["instanceStartTime"]) / 1000
    avgTime = int(
        ((int(time.time_ns() / 1000000) - states["botStartTime"]) / 1000)
        / (states["clearCount"] + states["fullClearCount"])
    )
    if states["instanceStartTime"] != -1:
        states["minTime"] = int(min(lastRun, states["minTime"]))
        states["maxTime"] = int(max(lastRun, states["maxTime"]))
    print(
        "floor 2 runs: {}, floor 3 runs: {}, bad run: {}, total death: {}, timeout runs: {}, dc: {}, crash: {}, restart: {}".format(
            states["clearCount"],
            states["fullClearCount"],
            states["badRunCount"],
            states["deathCount"],
            states["timeoutCount"],
            states["gameOfflineCount"],
            states["gameCrashCount"],
            states["gameRestartCount"],
        )
    )
    print(
        "Average time: {}, fastest time: {}, slowest time: {}".format(
            avgTime,
            states["minTime"],
            states["maxTime"],
        )
    )
    print(
        "gold portal count: {}, purple portal count: {}".format(
            states["goldPortalCount"], states["purplePortalCount"]
        )
    )


def useAbilities():
    while True:
        diedCheck()
        healthCheck()
        # windowCheck()
        if config["performance"] == False:
            clearQuest()
        if gameCrashCheck():
            return
        if offlineCheck():
            return
        if checkTimeout():
            return

        # check elite and mobs, lower priority cuz it only runs check once a cycle
        if states["status"] == "floor2" and not checkFloor2Elite() and checkFloor2Mob():
            calculateMinimapRelative(states["moveToX"], states["moveToY"])
            moveToMinimapRelative(states["moveToX"], states["moveToY"], 400, 500, False)
        elif states["status"] == "floor1" and not checkFloor2Mob():
            print("no mob on floor 1, random move to detect portal")
            randomMove()
            sleep(200, 250)
        elif (
            states["status"] == "floor2"
            and not checkFloor2Elite()
            and not checkFloor2Mob()
        ):
            print("no elite/mob on floor 2, random move to detect portal")
            randomMove()
            sleep(200, 250)
        elif states["status"] == "floor3" and checkFloor2Elite():
            calculateMinimapRelative(states["moveToX"], states["moveToY"])
            moveToMinimapRelative(states["moveToX"], states["moveToY"], 200, 300, False)
            # pydirectinput.press(config["awakening"])
        # elif (
        #     states["status"] == "floor2"
        #     and config["performance"] == True
        #     and checkFloor2Boss()
        # ):
        #     calculateMinimapRelative(states["moveToX"], states["moveToY"])
        #     moveToMinimapRelative(states["moveToX"], states["moveToY"], 950, 1050, True)
        #     fightFloor2Boss()

        # cast sequence
        for i in range(0, len(states["abilityScreenshots"])):
            if states["status"] == "floor3" and checkChaosFinish():
                return
            # diedCheck()
            healthCheck()

            # check portal
            if states["status"] == "floor3" and checkPortal():
                pydirectinput.click(
                    x=config["screenCenterX"],
                    y=config["screenCenterY"],
                    button=config["move"],
                )
                sleep(100, 150)
                checkPortal()
                return
            elif states["status"] == "floor2" and checkPortal():
                pydirectinput.click(
                    x=config["screenCenterX"],
                    y=config["screenCenterY"],
                    button=config["move"],
                )
                sleep(100, 150)
                checkPortal()
                return
            elif states["status"] == "floor1" and checkPortal():
                pydirectinput.click(
                    x=config["screenCenterX"],
                    y=config["screenCenterY"],
                    button=config["move"],
                )
                sleep(100, 150)
                checkPortal()
                return

            # click rift core
            if states["status"] == "floor3":
                clickTower()

            # check high-priority mobs
            if states["status"] == "floor1" and checkFloor2Mob():
                calculateMinimapRelative(states["moveToX"], states["moveToY"])
            elif states["status"] == "floor2":
                if config["performance"] == False and checkFloor2Boss():
                    calculateMinimapRelative(states["moveToX"], states["moveToY"])
                    moveToMinimapRelative(
                        states["moveToX"], states["moveToY"], 950, 1050, True
                    )
                    # fightFloor2Boss()
                elif (
                    config["performance"] == True
                    and (i == 3 or i == 5 or i == 7)
                    and checkFloor2Boss()
                ):
                    calculateMinimapRelative(states["moveToX"], states["moveToY"])
                    moveToMinimapRelative(
                        states["moveToX"], states["moveToY"], 950, 1050, True
                    )
                    # fightFloor2Boss()
                elif (i == 0 or i == 3 or i == 5) and checkFloor2Elite():
                    calculateMinimapRelative(states["moveToX"], states["moveToY"])
                    moveToMinimapRelative(
                        states["moveToX"], states["moveToY"], 750, 850, False
                    )
            elif states["status"] == "floor3" and checkFloor3GoldMob():
                calculateMinimapRelative(states["moveToX"], states["moveToY"])
                moveToMinimapRelative(
                    states["moveToX"], states["moveToY"], 700, 800, True
                )
                pydirectinput.press(config["awakening"])
                # pydirectinput.press(config["meleeAttack"])
            elif states["status"] == "floor3" and checkFloor3Tower():
                if not checkFloor2Elite() and not checkFloor2Mob():
                    randomMove()
                    checkFloor3Tower()
                calculateMinimapRelative(states["moveToX"], states["moveToY"])
                moveToMinimapRelative(
                    states["moveToX"], states["moveToY"], 1200, 1300, True
                )
                if (
                    config["characters"][states["currentCharacter"]]["class"]
                    == "sorceress"
                ):
                    pydirectinput.press("x")
                sleep(200, 220)
                clickTower()
            elif states["status"] == "floor3" and checkFloor2Mob():
                calculateMinimapRelative(states["moveToX"], states["moveToY"])
                moveToMinimapRelative(
                    states["moveToX"], states["moveToY"], 200, 300, False
                )
                # pydirectinput.press(config["awakening"])
            elif states["status"] == "floor3" and checkFloor2Boss():
                diedCheck()
                calculateMinimapRelative(states["moveToX"], states["moveToY"])
                moveToMinimapRelative(
                    states["moveToX"], states["moveToY"], 800, 900, False
                )

            """
            # # mage touch
            # if states["abilityScreenshots"][i]["key"] == config["mageTouch"]:
            #     x = 1080
            #     y = config["healthCheckY"]
            #     r, g, b = pyautogui.pixel(x, y)
            #     touchBuffActive = pyautogui.locateOnScreen(
            #         "./screenshots/touch.png",
            #         region=config["regions"]["buffs"],
            #         confidence=0.75,
            #     )
            #     if b > 70 and touchBuffActive != None:
            #         continue
            """

            # cast spells
            checkCDandCast(states["abilityScreenshots"][i])

        # 防止卡先试试这样
        if (
            states["status"] == "floor3"
            and not checkFloor2Elite()
            and not checkFloor2Boss()  # no random move in purple portal
        ):
            randomMove()


def checkCDandCast(ability):
    if config["characters"][states["currentCharacter"]]["class"] == "arcana":
        pydirectinput.press("x")
        pydirectinput.press("z")
    if (
        config["performance"] == True
        or config["GFN"] == True
        or pyautogui.locateOnScreen(
            ability["image"],
            region=config["regions"]["abilities"],
        )
    ):
        if ability["directional"] == True:
            pydirectinput.moveTo(x=states["moveToX"], y=states["moveToY"])
        else:
            pydirectinput.moveTo(x=config["screenCenterX"], y=config["screenCenterY"])

        if ability["cast"]:
            start_ms = int(time.time_ns() / 1000000)
            now_ms = int(time.time_ns() / 1000000)
            # spam until cast time before checking cd, to prevent 击倒后情况
            while now_ms - start_ms < ability["castTime"]:
                pydirectinput.press(ability["key"])
                now_ms = int(time.time_ns() / 1000000)
            # while pyautogui.locateOnScreen(
            #     ability["image"], region=config["regions"]["abilities"]
            # ):
            #     pydirectinput.press(ability["key"])
        elif ability["hold"]:
            # TODO: FIXME: avoid hold for now...
            start_ms = int(time.time_ns() / 1000000)
            now_ms = int(time.time_ns() / 1000000)
            pydirectinput.keyDown(ability["key"])
            while now_ms - start_ms < ability["holdTime"]:
                # pydirectinput.keyDown(ability["key"])
                now_ms = int(time.time_ns() / 1000000)
            pydirectinput.keyUp(ability["key"])
            # while pyautogui.locateOnScreen(
            #     ability["image"], region=config["regions"]["abilities"]
            # ):
            #     pydirectinput.keyDown(ability["key"])
            pydirectinput.keyUp(ability["key"])
        else:
            # 瞬发 ability
            pydirectinput.press(ability["key"])
            if config["performance"] == True or config["GFN"] == True:
                pydirectinput.press(ability["key"])
                sleep(50, 80)
                pydirectinput.press(ability["key"])
                sleep(50, 80)
                if states["status"] == "floor1":
                    sleep(300, 320)
                return
            start_ms = int(time.time_ns() / 1000000)
            now_ms = int(time.time_ns() / 1000000)
            while pyautogui.locateOnScreen(
                ability["image"],
                region=config["regions"]["abilities"],
            ):
                pydirectinput.press(ability["key"])
                sleep(50, 80)
                now_ms = int(time.time_ns() / 1000000)
                if now_ms - start_ms > 15000:
                    print("unable to use spell for 15s, check if disconnected")
                    return


def checkPortal():
    if config["performance"] == False:
        # check portal image
        portal = pyautogui.locateCenterOnScreen(
            "./screenshots/portal.png",
            region=config["regions"]["minimap"],
            confidence=0.7,
        )
        portalTop = pyautogui.locateCenterOnScreen(
            "./screenshots/portalTop.png",
            region=config["regions"]["minimap"],
            confidence=0.7,
        )
        portalBot = pyautogui.locateCenterOnScreen(
            "./screenshots/portalBot.png",
            region=config["regions"]["minimap"],
            confidence=0.7,
        )
        portalLeft = pyautogui.locateCenterOnScreen(
            "./screenshots/portalLeft.png",
            region=config["regions"]["minimap"],
            confidence=0.8,
        )
        portalRight = pyautogui.locateCenterOnScreen(
            "./screenshots/portalRight.png",
            region=config["regions"]["minimap"],
            confidence=0.8,
        )
        if portal != None:
            x, y = portal
            states["moveToX"] = x
            states["moveToY"] = y
            print(
                "portal image x: {} y: {}".format(states["moveToX"], states["moveToY"])
            )
            return True
        elif portalTop != None:
            x, y = portalTop
            states["moveToX"] = x
            states["moveToY"] = y + 7
            print(
                "portalTop image x: {} y: {}".format(
                    states["moveToX"], states["moveToY"]
                )
            )
            return True
        elif portalBot != None:
            x, y = portalBot
            states["moveToX"] = x
            states["moveToY"] = y - 7
            print(
                "portalBot image x: {} y: {}".format(
                    states["moveToX"], states["moveToY"]
                )
            )
            return True
        elif portalLeft != None:
            x, y = portalLeft
            states["moveToX"] = x + 3
            states["moveToY"] = y
            print(
                "portalLeft image x: {} y: {}".format(
                    states["moveToX"], states["moveToY"]
                )
            )
            return True
        elif portalRight != None:
            x, y = portalRight
            states["moveToX"] = x - 3
            states["moveToY"] = y
            print(
                "portalRight image x: {} y: {}".format(
                    states["moveToX"], states["moveToY"]
                )
            )
            return True

    # # only check with portal image at aor
    # if states["floor3Mode"] == True:
    #     return False

    minimap = pyautogui.screenshot(region=config["regions"]["minimap"])  # Top Right
    width, height = minimap.size
    order = spiralSearch(width, height, math.floor(width / 2), math.floor(height / 2))
    for entry in order:
        if entry[1] >= width or entry[0] >= height:
            continue
        r, g, b = minimap.getpixel((entry[1], entry[0]))
        inRange = False
        if config["GFN"] == True:
            inRange = (
                r in range(75, 105) and g in range(140, 170) and b in range(240, 256)
            ) or (
                r in range(120, 130) and g in range(210, 240) and b in range(240, 256)
            )
        else:
            inRange = (
                r in range(75, 85) and g in range(140, 150) and b in range(250, 256)
            ) or (
                r in range(120, 130) and g in range(210, 220) and b in range(250, 256)
            )
        if inRange:
            left, top, _w, _h = config["regions"]["minimap"]
            states["moveToX"] = left + entry[1]
            states["moveToY"] = top + entry[0]
            if r in range(75, 85) and g in range(140, 150) and b in range(250, 256):
                states["moveToY"] = states["moveToY"] - 1
            elif r in range(120, 130) and g in range(210, 220) and b in range(250, 256):
                states["moveToY"] = states["moveToY"] + 1
            print(
                "portal pixel x: {} y: {}, r: {} g: {} b: {}".format(
                    states["moveToX"], states["moveToY"], r, g, b
                )
            )
            return True
    return False


def checkFloor2Elite():
    minimap = pyautogui.screenshot(region=config["regions"]["minimap"])  # Top Right
    width, height = minimap.size
    order = spiralSearch(width, height, math.floor(width / 2), math.floor(height / 2))
    for entry in order:
        if entry[1] >= width or entry[0] >= height:
            continue
        r, g, b = minimap.getpixel((entry[1], entry[0]))
        inRange = False
        if config["GFN"] == True:
            inRange = (
                r in range(180, 215)
                and g in range(125, 150)
                and b in range(60, 80)
                # or r in range(90, 110)
                # and g in range(55, 70)
                # and b in range(10, 40)
            )
        else:
            inRange = (
                r in range(190, 215) and g in range(125, 150) and b in range(30, 70)
            )
        if inRange:
            left, top, _w, _h = config["regions"]["minimap"]
            states["moveToX"] = left + entry[1]
            states["moveToY"] = top + entry[0]
            print(
                "elite x: {} y: {}, r: {} g: {} b: {}".format(
                    states["moveToX"], states["moveToY"], r, g, b
                )
            )
            return True
    return False


def checkFloor2Mob():
    minimap = pyautogui.screenshot(region=config["regions"]["minimap"])  # Top Right
    width, height = minimap.size
    order = spiralSearch(width, height, math.floor(width / 2), math.floor(height / 2))
    if states["status"] == "floor2":
        order = reversed(order)
    for entry in order:
        if entry[1] >= width or entry[0] >= height:
            continue
        r, g, b = minimap.getpixel((entry[1], entry[0]))
        inRange = False
        if config["GFN"] == True:
            inRange = (
                (r in range(180, 215)) and (g in range(17, 35)) and (b in range(17, 55))
            )
        else:
            inRange = r == 208 and g == 24 and b == 24
        if inRange:
            left, top, _w, _h = config["regions"]["minimap"]
            states["moveToX"] = left + entry[1]
            states["moveToY"] = top + entry[0]
            print(
                "mob x: {} y: {}, r: {} g: {} b: {}".format(
                    states["moveToX"], states["moveToY"], r, g, b
                )
            )
            return True
    return False


def checkFloor3GoldMob():
    minimap = pyautogui.screenshot(region=config["regions"]["minimap"])  # Top Right
    width, height = minimap.size
    order = spiralSearch(width, height, math.floor(width / 2), math.floor(height / 2))
    for entry in order:
        if entry[1] >= width or entry[0] >= height:
            continue
        r, g, b = minimap.getpixel((entry[1], entry[0]))
        inRange = False
        if config["GFN"] == True:
            inRange = (
                (r in range(242, 256))
                and (g in range(181, 196))
                and (b in range(29, 40))
            )
        else:
            inRange = r == 255 and g == 188 and b == 30
        if inRange:
            left, top, _w, _h = config["regions"]["minimap"]
            states["moveToX"] = left + entry[1]
            states["moveToY"] = top + entry[0]
            print(
                "gold x: {} y: {}, r: {} g: {} b: {}".format(
                    states["moveToX"], states["moveToY"], r, g, b
                )
            )
            return True
    return False


def checkFloor2Boss():
    fightFloor2Boss()
    bossLocation = pyautogui.locateCenterOnScreen(
        "./screenshots/boss.png", confidence=0.65, region=config["regions"]["minimap"]
    )
    if bossLocation != None:
        left, top = bossLocation
        states["moveToX"] = left
        states["moveToY"] = top
        print("boss x: {} y: {}".format(states["moveToX"], states["moveToY"]))
        return True
    return False


# def checkFloor2Boss():
#     sleep(100, 200)
#     fightFloor2Boss()
#     minimap = pyautogui.screenshot(region=config["regions"]["minimap"])  # Top Right
#     width, height = minimap.size
#     order = spiralSearch(width, height, math.floor(width / 2), math.floor(height / 2))
#     for entry in order:
#         if entry[1] >= width or entry[0] >= height:
#             continue
#         r, g, b = minimap.getpixel((entry[1], entry[0]))
#         if (
#             (r in range(153, 173)) and (g in range(25, 35)) and (b in range(25, 35))
#         ):  # r == 199 and g == 28 and b == 30
#             left, top, _w, _h = config["regions"]["minimap"]
#             states["moveToX"] = left + entry[1]
#             states["moveToY"] = top + entry[0]
#             print(
#                 "Boss x: {} y: {}, r: {} g: {} b: {}".format(
#                     states["moveToX"], states["moveToY"], r, g, b
#                 )
#             )
#             return True


def clickTower():
    riftCore1 = pyautogui.locateCenterOnScreen(
        "./screenshots/riftcore1.png",
        confidence=0.6,
        region=config["regions"]["portal"],
    )
    riftCore2 = pyautogui.locateCenterOnScreen(
        "./screenshots/riftcore2.png",
        confidence=0.6,
        region=config["regions"]["portal"],
    )
    if riftCore1 != None:
        x, y = riftCore1
        if y > 650 or x < 400 or x > 1500:
            return
        states["moveToX"] = x
        states["moveToY"] = y + 190
        pydirectinput.click(
            x=states["moveToX"], y=states["moveToY"], button=config["move"]
        )
        print("clicked rift core")
        sleep(100, 120)
        pydirectinput.press(config["meleeAttack"])
        sleep(300, 360)
        pydirectinput.press(config["meleeAttack"])
        sleep(300, 360)
        pydirectinput.press(config["meleeAttack"])
        sleep(100, 120)
        pydirectinput.press(config["meleeAttack"])
    elif riftCore2 != None:
        x, y = riftCore2
        if y > 650 or x < 400 or x > 1500:
            return
        states["moveToX"] = x
        states["moveToY"] = y + 190
        pydirectinput.click(
            x=states["moveToX"], y=states["moveToY"], button=config["move"]
        )
        print("clicked rift core")
        sleep(100, 120)
        pydirectinput.press(config["meleeAttack"])
        sleep(300, 360)
        pydirectinput.press(config["meleeAttack"])
        sleep(300, 360)
        pydirectinput.press(config["meleeAttack"])
        sleep(100, 120)
        pydirectinput.press(config["meleeAttack"])


def checkFloor3Tower():
    # TODO: partial tower
    tower = pyautogui.locateCenterOnScreen(
        "./screenshots/tower.png", region=config["regions"]["minimap"], confidence=0.7
    )
    towerTop = pyautogui.locateCenterOnScreen(
        "./screenshots/towerTop.png",
        region=config["regions"]["minimap"],
        confidence=0.6,
    )
    towerBot = pyautogui.locateCenterOnScreen(
        "./screenshots/towerBot.png",
        region=config["regions"]["minimap"],
        confidence=0.6,
    )
    if tower != None:
        x, y = tower
        states["moveToX"] = x
        states["moveToY"] = y
        print("tower image x: {} y: {}".format(states["moveToX"], states["moveToY"]))
        return True
    elif towerTop != None:
        x, y = towerTop
        states["moveToX"] = x
        states["moveToY"] = y + 7
        print("towerTop image x: {} y: {}".format(states["moveToX"], states["moveToY"]))
        return True
    elif towerBot != None:
        x, y = towerBot
        states["moveToX"] = x
        states["moveToY"] = y - 7
        print("towerBot image x: {} y: {}".format(states["moveToX"], states["moveToY"]))
        return True

    minimap = pyautogui.screenshot(region=config["regions"]["minimap"])  # Top Right
    width, height = minimap.size
    order = spiralSearch(width, height, math.floor(width / 2), math.floor(height / 2))
    for entry in order:
        if entry[1] >= width or entry[0] >= height:
            continue
        r, g, b = minimap.getpixel((entry[1], entry[0]))
        inRange = False
        if config["GFN"] == True:
            inRange = (
                r in range(209, 229) and g in range(40, 60) and b in range(49, 69)
            ) or (
                r in range(245, 256) and g in range(163, 173) and b in range(179, 189)
            )
        else:
            inRange = (
                r in range(209, 229) and g in range(40, 60) and b in range(49, 69)
            ) or (r == 162 and g == 162 and b == 162)
            (r in range(245, 255) and g in range(163, 173) and b in range(179, 189))
        if inRange:
            left, top, _w, _h = config["regions"]["minimap"]
            states["moveToX"] = left + entry[1]
            states["moveToY"] = top + entry[0]
            # pos offset
            if r in range(245, 256) and g in range(163, 173) and b in range(179, 189):
                states["moveToY"] = states["moveToY"] + 1
            print(
                "tower pixel pos x: {} y: {}, r: {} g: {} b: {}".format(
                    states["moveToX"], states["moveToY"], r, g, b
                )
            )
            return True

    return False


def checkChaosFinish():
    clearOk = pyautogui.locateCenterOnScreen(
        "./screenshots/clearOk.png", confidence=0.75, region=(625, 779, 500, 155)
    )
    if clearOk != None:
        states["fullClearCount"] = states["fullClearCount"] + 1
        x, y = clearOk
        pydirectinput.moveTo(x=x, y=y)
        sleep(600, 800)
        pydirectinput.click(x=x, y=y, button="left")
        sleep(200, 300)
        pydirectinput.moveTo(x=x, y=y)
        sleep(200, 300)
        pydirectinput.click(x=x, y=y, button="left")
        return True
    return False


def fightFloor2Boss():
    if pyautogui.locateOnScreen(
        "./screenshots/bossBar.png", confidence=0.7, region=(406, 159, 1000, 200)
    ):
        print("boss bar located")
        # pydirectinput.moveTo(x=states["moveToX"], y=states["moveToY"])
        # sleep(80, 100)
        pydirectinput.press(config["awakening"])


def calculateMinimapRelative(x, y):
    selfLeft = config["minimapCenterX"]
    selfTop = config["minimapCenterY"]
    # if abs(selfLeft - x) <= 3 and abs(selfTop - y) <= 3:
    #     states["moveToX"] = config["screenCenterX"]
    #     states["moveToY"] = config["screenCenterY"]
    #     return

    x = x - selfLeft
    y = y - selfTop
    distBtwPoints = math.sqrt(x * x + y * y)
    states["moveTime"] = int(distBtwPoints * 16)

    dist = 200
    if y < 0:
        dist = -dist

    if x == 0:
        if y < 0:
            newY = y - abs(dist)
        else:
            newY = y + abs(dist)
        # print("relative to center pos newX: 0 newY: {}".format(int(newY)))
        states["moveToX"] = 0 + config["screenCenterX"]
        states["moveToY"] = int(newY) + config["screenCenterY"]
        return
    if y == 0:
        if x < 0:
            newX = x - abs(dist)
        else:
            newX = x + abs(dist)
        # print("relative to center pos newX: {} newY: 0".format(int(newX)))
        states["moveToX"] = int(newX) + config["screenCenterX"]
        states["moveToY"] = 0 + config["screenCenterY"]
        return

    k = y / x
    # newX = x + dist
    newY = y + dist
    # newY = k * (newX - x) + y
    newX = (newY - y) / k + x

    # print("before confining newX: {} newY: {}".format(int(newX), int(newY)))
    if newX < 0 and abs(newX) > config["clickableAreaX"]:
        newX = -config["clickableAreaX"]
        if newY < 0:
            newY = newY + abs(dist) * 0.25
        else:
            newY = newY - abs(dist) * 0.25
    elif newX > 0 and abs(newX) > config["clickableAreaX"]:
        newX = config["clickableAreaX"]
        if newY < 0:
            newY = newY + abs(dist) * 0.25
        else:
            newY = newY - abs(dist) * 0.25

    if newY < 0 and abs(newY) > config["clickableAreaY"]:
        newY = -config["clickableAreaY"]
        if newX < 0:
            newX = newX + abs(dist) * 0.7
        else:
            newX = newX - abs(dist) * 0.7
    elif newY > 0 and abs(newY) > config["clickableAreaY"]:
        newY = config["clickableAreaY"]
        if newX < 0:
            newX = newX + abs(dist) * 0.7
        else:
            newX = newX - abs(dist) * 0.7

    # print(
    #     "after confining relative to center pos newX: {} newY: {}".format(
    #         int(newX), int(newY)
    #     )
    # )
    states["moveToX"] = int(newX) + config["screenCenterX"]
    states["moveToY"] = int(newY) + config["screenCenterY"]
    return


def moveToMinimapRelative(x, y, timeMin, timeMax, blink):
    # move one step to direction
    if (
        states["moveToX"] == config["screenCenterX"]
        and states["moveToY"] == config["screenCenterY"]
    ):
        return
    print("moving to pos x: {} y: {}".format(states["moveToX"], states["moveToY"]))

    # count = 0
    # turn = True
    # deflect = 60

    if states["status"] == "floor1":
        pydirectinput.moveTo(x=x, y=y)
        return

    # moving in a straight line
    if states["moveTime"] < 50:
        return
    # print("move for {} ms".format(states["moveTime"]))
    pydirectinput.keyDown("alt")
    sleep(10, 30)
    pydirectinput.click(x=x, y=y, button=config["move"])
    sleep(10, 30)
    pydirectinput.keyUp("alt")
    sleep(int(states["moveTime"] / 2) - 50, int(states["moveTime"] / 2) + 50)

    # moving in a straight line
    pydirectinput.keyDown("alt")
    sleep(10, 30)
    pydirectinput.click(x=x, y=y, button=config["move"])
    sleep(10, 30)
    pydirectinput.keyUp("alt")
    sleep(int(states["moveTime"] / 2) - 50, int(states["moveTime"] / 2) + 50)

    # sleep(timeMin, timeMax)

    # optional blink here
    if blink or states["moveTime"] > 800:
        # print("blink")
        if states["moveTime"] > 1200:
            if config["characters"][states["currentCharacter"]]["class"] == "sorceress":
                pydirectinput.press("x")
            sleep(300, 320)
        pydirectinput.press(config["blink"])
        sleep(300, 320)

    return

    # # snake moving
    # while count < 3:
    #     if x > 960 and y < 540:
    #         if turn:
    #             x = x - deflect* 2.5
    #             y = y - deflect
    #         else:
    #             x = x + deflect* 2.5
    #             y = y + deflect
    #     elif x > 960 and y > 540:
    #         if turn:
    #             x = x + deflect* 2.5
    #             y = y - deflect
    #         else:
    #             x = x - deflect * 2.5
    #             y = y + deflect
    #     elif x < 960 and y > 540:
    #         if turn:
    #             x = x + deflect* 2.5
    #             y = y + deflect
    #         else:
    #             x = x - deflect* 2.5
    #             y = y - deflect
    #     elif x < 960 and y < 540:
    #         if turn:
    #             x = x - deflect* 2.5
    #             y = y + deflect
    #         else:
    #             x = x + deflect* 2.5
    #             y = y - deflect
    #     pydirectinput.click(x=x, y=y, button=config['move'])
    #     sleep(math.floor(timeMin / 3), math.floor(timeMax / 3))
    #     turn = not turn
    #     count = count + 1


def randomMove():
    x = random.randint(
        config["screenCenterX"] - config["clickableAreaX"],
        config["screenCenterX"] + config["clickableAreaX"],
    )
    y = random.randint(
        config["screenCenterY"] - config["clickableAreaY"],
        config["screenCenterY"] + config["clickableAreaY"],
    )

    print("random move to x: {} y: {}".format(x, y))
    pydirectinput.click(x=x, y=y, button=config["move"])
    sleep(200, 250)
    pydirectinput.click(x=x, y=y, button=config["move"])
    sleep(200, 250)
    pydirectinput.click(
        x=config["screenCenterX"], y=config["screenCenterY"], button=config["move"]
    )
    sleep(200, 250)


# def isPortalFlame(image, x, y):
#     r, g, b = image.getpixel((x, y))
#     flag = False
#     dist = 5
#     blueFlag = r in range(1, 3) and g in range(1, 4) and b in range(3, 6)
#     purpleFlag = r in range(3, 6) and g in range(1, 4) and b in range(1, 3)
#     if blueFlag or purpleFlag:
#         return True
#     return flag


def enterPortal():
    # repeatedly move and press g until black screen
    sleep(1100, 1200)
    print("moving to portal x: {} y: {}".format(states["moveToX"], states["moveToY"]))
    print("move for {} ms".format(states["moveTime"]))
    if states["moveTime"] > 550:
        # print("blink")
        pydirectinput.click(
            x=states["moveToX"], y=states["moveToY"], button=config["move"]
        )
        sleep(100, 150)
        pydirectinput.press(config["blink"])

    enterTime = int(time.time_ns() / 1000000)
    while True:
        nowTime = int(time.time_ns() / 1000000)
        if nowTime - enterTime > 3000:
            # FIXME:
            # states["instanceStartTime"] = -1
            # badRun = pyautogui.screenshot()
            # badRun.save("./debug/badRun_" + str(nowTime) + ".png")
            # states["badRunCount"] = states["badRunCount"] + 1
            pydirectinput.moveTo(x=config["screenCenterX"], y=config["screenCenterY"])
            sleep(100, 150)
            pydirectinput.click(
                x=config["screenCenterX"],
                y=config["screenCenterY"],
                button=config["move"],
            )
            sleep(100, 150)
            return False

        # if states["status"] == "floor2" or states["status"] == "floor3":
        #     portalArea = pyautogui.screenshot(region=config["regions"]["portal"])
        #     width, height = portalArea.size
        #     order = spiralSearch(
        #         width, height, math.floor(width / 2), math.floor(height / 2)
        #     )
        #     for entry in order:
        #         if entry[1] >= width or entry[0] >= height:
        #             continue
        #         if isPortalFlame(portalArea, entry[1], entry[0]):
        #             left, top, _w, _h = config["regions"]["portal"]
        #             states["moveToX"] = left + entry[1]
        #             states["moveToY"] = top + entry[0]
        #             print(
        #                 "portal flame x: {} y: {}".format(
        #                     states["moveToX"], states["moveToY"]
        #                 )
        #             )
        #             pydirectinput.press(config["interact"])
        #             pydirectinput.click(
        #                 x=states["moveToX"], y=states["moveToY"], button=config["move"]
        #             )
        #             im = pyautogui.screenshot(region=(1652, 168, 240, 210))
        #             r, g, b = im.getpixel((1772 - 1652, 272 - 168))
        #             while r != 0 or g != 0 or b != 0:
        #                 pydirectinput.press(config["interact"])
        #                 sleep(50, 60)
        #                 nowTime = int(time.time_ns() / 1000000)
        #                 if nowTime - enterTime > 10000:
        #                     # FIXME:
        #                     states["instanceStartTime"] = -1
        #                     return
        #             print("portal entered")
        #             return

        # portalFlame = pyautogui.locateCenterOnScreen(
        #     "./screenshots/portalFlame.png",
        #     grayscale=True,
        #     confidence=0.3,
        # )
        # if portalFlame != None:
        #     x, y = portalFlame
        #     pydirectinput.press(config["interact"])
        #     pydirectinput.click(x=x, y=y, button=config["move"])
        #     im = pyautogui.screenshot(region=(1652, 168, 240, 210))
        #     r, g, b = im.getpixel((1772 - 1652, 272 - 168))
        #     while r != 0 or g != 0 or b != 0:
        #         pydirectinput.press(config["interact"])
        #         sleep(50, 60)

        #         nowTime = int(time.time_ns() / 1000000)
        #         if nowTime - enterTime > 10000:
        #             # FIXME:
        #             states["instanceStartTime"] = -1
        #             return
        #     print("portal entered")
        #     return

        if (
            states["moveToX"] == config["screenCenterX"]
            and states["moveToY"] == config["screenCenterY"]
        ):
            pydirectinput.press(config["interact"])
            sleep(100, 120)
        else:
            pydirectinput.press(config["interact"])
            pydirectinput.click(
                x=states["moveToX"], y=states["moveToY"], button=config["move"]
            )
            pydirectinput.press(config["interact"])
            sleep(60, 70)

        # try to enter portal until black screen
        im = pyautogui.screenshot(region=(1652, 168, 240, 210))
        r, g, b = im.getpixel((1772 - 1652, 272 - 168))
        if r + g + b < 10:
            print("portal entered")
            pydirectinput.moveTo(x=config["screenCenterX"], y=config["screenCenterY"])
            return True


# def enterPortal():
#     # repeatedly move and press g until black screen
#     print("moving to portal x: {} y: {}".format(states["moveToX"], states["moveToY"]))
#     turn = True
#     deflect = 80
#     while True:
#         im = pyautogui.screenshot(region=(1652, 168, 240, 210))
#         r, g, b = im.getpixel((1772 - 1652, 272 - 168))
#         if r == 0 and g == 0 and b == 0:
#             return

#         x = states["moveToX"]
#         y = states["moveToY"]
#         if x > 960 and y < 540:
#             if turn:
#                 x = x - deflect * 2.5
#                 y = y - deflect
#             else:
#                 x = x + deflect * 2.5
#                 y = y + deflect
#         elif x > 960 and y > 540:
#             if turn:
#                 x = x + deflect * 2.5
#                 y = y - deflect
#             else:
#                 x = x - deflect * 2.5
#                 y = y + deflect
#         elif x < 960 and y > 540:
#             if turn:
#                 x = x + deflect * 2.5
#                 y = y + deflect
#             else:
#                 x = x - deflect * 2.5
#                 y = y - deflect
#         elif x < 960 and y < 540:
#             if turn:
#                 x = x - deflect * 2.5
#                 y = y + deflect
#             else:
#                 x = x + deflect * 2.5
#                 y = y - deflect
#         # print('movex: {} movey: {} x:{} y: {} turn: {}'.format(states['moveToX'], states['moveToY'], x,y,turn))
#         count = 0
#         while count < 5:
#             pydirectinput.press(config["interact"])
#             im = pyautogui.screenshot(region=(1652, 168, 240, 210))
#             r, g, b = im.getpixel((1772 - 1652, 272 - 168))
#             if r == 0 and g == 0 and b == 0:
#                 return

#             if (
#                 states["moveToX"] == config["screenCenterX"]
#                 and states["moveToY"] == config["screenCenterY"]
#             ):
#                 pydirectinput.press(config["interact"])
#                 sleep(100, 120)
#             else:
#                 pydirectinput.click(x=x, y=y, button=config["move"])
#                 sleep(50, 60)
#                 pydirectinput.press(config["interact"])
#                 count = count + 1
#             turn = not turn
#     return


def waitForLoading():
    print("loading")
    blackScreenStartTime = int(time.time_ns() / 1000000)
    while True:
        if offlineCheck():
            closeGameByClickingDialogue()
            return
        if gameCrashCheck():
            return
        currentTime = int(time.time_ns() / 1000000)
        if currentTime - blackScreenStartTime > config["blackScreenTimeLimit"]:
            pyautogui.hotkey("alt", "f4")
            pydirectinput.keyDown("alt")
            sleep(350, 400)
            pydirectinput.keyDown("f4")
            sleep(350, 400)
            pydirectinput.keyUp("alt")
            sleep(350, 400)
            pydirectinput.keyUp("f4")
            sleep(350, 400)
            sleep(10000, 15000)
            return
        leaveButton = pyautogui.locateOnScreen(
            "./screenshots/leave.png",
            grayscale=True,
            confidence=0.7,
            region=config["regions"]["leaveMenu"],
        )
        if leaveButton != None:
            return
        sleep(350, 400)


def saveAbilitiesScreenshots():
    for ability in abilities[config["characters"][states["currentCharacter"]]["class"]]:
        if ability["abilityType"] == "awakening":
            continue
        if ability["abilityType"] == "specialty1":
            continue
        if ability["abilityType"] == "specialty2":
            continue
        left = ability["position"]["left"]
        top = ability["position"]["top"]
        width = ability["position"]["width"]
        height = ability["position"]["height"]
        im = pyautogui.screenshot(region=(left, top, width, height))
        states["abilityScreenshots"].append(
            {
                "key": ability["key"],
                "image": im,
                "cast": ability["cast"],
                "castTime": ability["castTime"],
                "hold": ability["hold"],
                "holdTime": ability["holdTime"],
                "directional": ability["directional"],
            }
        )
        sleep(200, 300)


# def windowCheck():
#     if pyautogui.locateOnScreen(
#         "./screenshots/close.png", grayscale=True, confidence=0.9
#     ):
#         pydirectinput.press("esc")
#         sleep(500, 600)


def diedCheck():  # get information about wait a few second to revive
    if pyautogui.locateOnScreen(
        "./screenshots/died.png",
        grayscale=True,
        confidence=0.9,
        region=(917, 145, 630, 550),
    ):
        states["deathCount"] = states["deathCount"] + 1
        sleep(5000, 5500)
        while (
            pyautogui.locateOnScreen(
                "./screenshots/resReady.png",
                confidence=0.7,
                region=(917, 145, 630, 550),
            )
            != None
        ):
            pydirectinput.moveTo(1275, 454)
            sleep(600, 800)
            pydirectinput.click(1275, 454, button="left")
            sleep(600, 800)
            pydirectinput.moveTo(config["screenCenterX"], config["screenCenterY"])
            sleep(600, 800)
            if gameCrashCheck():
                return
            if offlineCheck():
                return
            if checkTimeout():
                return
    return


def doAuraRepair(forced):
    # Check if repair needed
    if forced or pyautogui.locateOnScreen(
        "./screenshots/repair.png",
        grayscale=True,
        confidence=0.4,
        region=(1500, 134, 100, 100),
    ):
        print("repairing")
        pydirectinput.keyDown("alt")
        sleep(800, 900)
        pydirectinput.press("p")
        sleep(800, 900)
        pydirectinput.keyUp("alt")
        sleep(800, 900)
        pydirectinput.moveTo(1142, 661)
        sleep(600, 700)
        pydirectinput.click(1142, 661, button="left")
        sleep(600, 700)
        pydirectinput.moveTo(1054, 455)
        sleep(600, 700)
        pydirectinput.click(1054, 455, button="left")
        sleep(600, 700)
        pydirectinput.press("esc")
        sleep(800, 900)
        pydirectinput.press("esc")
        sleep(800, 900)


def doCityRepair():
    # for non-aura users: MUST have your character parked near a repairer in city before starting the script
    # Check if repair needed
    if pyautogui.locateOnScreen(
        "./screenshots/repair.png",
        grayscale=True,
        confidence=0.4,
        region=(1500, 134, 100, 100),
    ):
        print("repairing")
        pydirectinput.press("g")
        sleep(600, 700)
        pydirectinput.moveTo(1057, 455)
        sleep(600, 700)
        pydirectinput.click(1057, 455, button="left")
        sleep(600, 700)
        pydirectinput.press("esc")
        sleep(1500, 1900)


def healthCheck():
    if config["useHealthPot"] == False:
        return
    x = int(
        config["healthCheckX"]
        + (870 - config["healthCheckX"]) * config["healthPotAtPercent"]
    )
    y = config["healthCheckY"]
    r, g, b = pyautogui.pixel(x, y)
    # print(x, r, g, b)
    if r < 70:
        leaveButton = pyautogui.locateCenterOnScreen(
            "./screenshots/leave.png",
            grayscale=True,
            confidence=0.7,
            region=config["regions"]["leaveMenu"],
        )
        if leaveButton == None:
            return
        pydirectinput.press(config["healthPot"])
        states["healthPotCount"] = states["healthPotCount"] + 1
        return
    return


def clearQuest():
    quest = pyautogui.locateCenterOnScreen(
        "./screenshots/quest.png", confidence=0.9, region=(815, 600, 250, 200)
    )
    leveledup = pyautogui.locateCenterOnScreen(
        "./screenshots/leveledup.png", confidence=0.9, region=(815, 600, 250, 200)
    )
    gameMenu = pyautogui.locateCenterOnScreen(
        "./screenshots/gameMenu.png",
        confidence=0.95,
        region=config["regions"]["center"],
    )
    if gameMenu != None:
        print("game menu detected")
        pydirectinput.press("esc")
        sleep(1800, 1900)
    if quest != None:
        print("clear quest")
        x, y = quest
        pydirectinput.moveTo(x=x, y=y)
        sleep(1800, 1900)
        pydirectinput.click(x=x, y=y, button="left")
        sleep(1800, 1900)
        pydirectinput.press("esc")
        sleep(1800, 1900)
    elif leveledup != None:
        print("clear level")
        x, y = leveledup
        pydirectinput.moveTo(x=x, y=y)
        sleep(1800, 1900)
        pydirectinput.click(x=x, y=y, button="left")
        sleep(1800, 1900)
        pydirectinput.press("esc")
        sleep(1800, 1900)


def sleep(min, max):
    sleepTime = random.randint(min, max) / 1000.0
    if sleepTime < 0:
        return
    time.sleep(sleepTime)


def spiralSearch(rows, cols, rStart, cStart):
    ans = []  # 可以通过长度来退出返回
    end = rows * cols  # 边界扩张
    i = i1 = i2 = rStart
    # 分别是当前点,上下边界的上边界，下边界
    j = j1 = j2 = cStart  # 当前，左、右边界
    while True:
        j2 += 1
        while j < j2:
            if 0 <= j < cols and 0 <= i:  # i刚减完
                ans.append([i, j])
            j += 1
            if 0 > i:  # i超过了，跳过优化
                j = j2  # 没有答案可添加
        i2 += 1
        while i < i2:
            if 0 <= i < rows and j < cols:
                ans.append([i, j])
            i += 1
            if j >= cols:
                i = i2
        j1 -= 1
        while j > j1:
            if 0 <= j < cols and i < rows:
                ans.append([i, j])
            j -= 1
            if i >= rows:
                j = j1
        i1 -= 1
        while i > i1:
            if 0 <= i < rows and 0 <= j:
                ans.append([i, j])
            i -= 1
            if 0 > j:
                i = i1
        if len(ans) == end:
            return ans


def checkTimeout():
    currentTime = int(time.time_ns() / 1000000)
    # hacky way of quitting
    if states["instanceStartTime"] == -1:
        print("hacky timeout")
        return True
    if currentTime - states["instanceStartTime"] > config["timeLimit"]:
        print("timeout triggered")
        timeout = pyautogui.screenshot()
        timeout.save("./debug/timeout_" + str(currentTime) + ".png")
        states["timeoutCount"] = states["timeoutCount"] + 1
        return True
    return False


def gameCrashCheck():
    bottom = pyautogui.screenshot(region=(800, 960, 250, 50))
    r1, g1, b1 = bottom.getpixel((0, 0))
    r2, g2, b2 = bottom.getpixel((0, 49))
    r3, g3, b3 = bottom.getpixel((249, 0))
    r4, g4, b4 = bottom.getpixel((249, 49))
    sum = r1 + g1 + b1 + r2 + g2 + b2 + r3 + g3 + b3 + r4 + g4 + b4
    if sum > 10:
        print("game crashed, restarting game client...")
        states["gameCrashCount"] = states["gameCrashCount"] + 1
        return True
    return False


def offlineCheck():
    dc = pyautogui.locateOnScreen(
        "./screenshots/dc.png",
        region=config["regions"]["center"],
        confidence=config["confidenceForGFN"],
    )
    ok = pyautogui.locateCenterOnScreen(
        "./screenshots/ok.png", region=config["regions"]["center"], confidence=0.75
    )
    enterServer = pyautogui.locateCenterOnScreen(
        "./screenshots/enterServer.png",
        confidence=config["confidenceForGFN"],
        region=(885, 801, 160, 55),
    )
    if config["GFN"] == True:
        sessionLimitReached = pyautogui.locateCenterOnScreen(
            "./screenshots/sessionLimitReached.png",
            region=config["regions"]["center"],
            confidence=0.9,
        )
        if sessionLimitReached != None:
            pydirectinput.moveTo(x=1029, y=822)
            sleep(1300, 1400)
            pydirectinput.click(x=1029, y=822, button="left")
            sleep(1300, 1400)
            return True
    if dc != None or ok != None or enterServer != None:
        currentTime = int(time.time_ns() / 1000000)
        dc = pyautogui.screenshot()
        dc.save("./debug/dc_" + str(currentTime) + ".png")
        print(
            "disconnection detected...currentTime : {} dc:{} ok:{} enterServer:{}".format(
                currentTime, dc, ok, enterServer
            )
        )
        states["gameOfflineCount"] = states["gameOfflineCount"] + 1
        return True
    return False


def closeGameByClickingDialogue():
    """
    # ok = pyautogui.locateCenterOnScreen(
    #     "./screenshots/ok.png",
    #     region=config["regions"]["center"],
    # )
    # if ok != None:
    #     x, y = ok
    #     pydirectinput.moveTo(x=x, y=y)
    #     sleep(300, 400)
    #     pydirectinput.click(x=x, y=y, button="left")
    # else:
    #     pydirectinput.moveTo(x=960, y=500)
    #     sleep(300, 400)
    #     pydirectinput.click(button="left")
    """
    while True:
        ok = pyautogui.locateCenterOnScreen(
            "./screenshots/ok.png", region=config["regions"]["center"], confidence=0.75
        )
        enterServer = pyautogui.locateCenterOnScreen(
            "./screenshots/enterServer.png",
            confidence=config["confidenceForGFN"],
            region=(885, 801, 160, 55),
        )
        if ok != None:
            x, y = ok
            pydirectinput.moveTo(x=x, y=y)
            sleep(300, 400)
            pydirectinput.click(x=x, y=y, button="left")
            print("clicked ok")
        elif enterServer != None:
            break
        else:
            break
        sleep(1300, 1400)
    states["status"] = "restart"
    sleep(12000, 13000)


def restartGame():
    print("restart game")
    states["multiCharacterMode"] = False  # for now
    states["multiCharacterModeState"] = []  # for now
    states["currentCharacter"] = config["mainCharacter"]
    while True:
        enterGame = pyautogui.locateCenterOnScreen(
            "./screenshots/steamPlay.png", confidence=0.75
        )
        sleep(500, 600)
        stopGame = pyautogui.locateCenterOnScreen(
            "./screenshots/steamStop.png", confidence=0.75
        )
        sleep(500, 600)
        confirm = pyautogui.locateCenterOnScreen(
            "./screenshots/steamConfirm.png", confidence=0.75
        )
        sleep(500, 600)
        enterServer = pyautogui.locateCenterOnScreen(
            "./screenshots/enterServer.png",
            confidence=config["confidenceForGFN"],
            region=(885, 801, 160, 55),
        )
        sleep(500, 600)
        inTown = pyautogui.locateCenterOnScreen(
            "./screenshots/inTown.png",
            confidence=0.75,
            region=(1870, 133, 25, 30),
        )
        if stopGame != None:
            print("clicking stop game on steam")
            x, y = stopGame
            pydirectinput.moveTo(x=x, y=y)
            sleep(1200, 1300)
            pydirectinput.click(x=x, y=y, button="left")
            sleep(500, 600)
            confirm = pyautogui.locateCenterOnScreen(
                "./screenshots/steamConfirm.png", confidence=0.75
            )
            if confirm == None:
                continue
            x, y = confirm
            pydirectinput.moveTo(x=x, y=y)
            sleep(1200, 1300)
            pydirectinput.click(x=x, y=y, button="left")
            sleep(10000, 12000)
        elif confirm != None:
            print("confirming stop game")
            x, y = confirm
            pydirectinput.moveTo(x=x, y=y)
            sleep(1200, 1300)
            pydirectinput.click(x=x, y=y, button="left")
            sleep(10000, 12000)
        elif enterGame != None:
            print("restarting Lost Ark game client...")
            x, y = enterGame
            pydirectinput.moveTo(x=x, y=y)
            sleep(1200, 1300)
            pydirectinput.click(x=x, y=y, button="left")
            break
        elif enterServer != None:
            # new eacoffline interface
            break
        elif inTown != None:
            return
        elif config["GFN"] == True:
            sleep(10000, 12000)
            # TODO: handle potential crash on GFN
            loaGFN = pyautogui.locateCenterOnScreen(
                "./screenshots/loaGFN.png",
                confidence=0.8,
            )
            if loaGFN != None:
                x, y = loaGFN
                pydirectinput.moveTo(x=x, y=y)
                sleep(2200, 2300)
                pydirectinput.click(x=x, y=y, button="left")
                sleep(40000, 42000)
                break
            # # i think eventually GFN would restart?
            # loa = pyautogui.locateCenterOnScreen(
            #     "./screenshots/loa.png",
            #     confidence=0.8,
            # )
            # if loa != None:
            #     x, y = loa
            #     pydirectinput.moveTo(x=x, y=y)
            #     sleep(1200, 1300)
            #     pydirectinput.click(x=x, y=y, button="left")
            #     sleep(2200, 2300)
            #     continue
        sleep(1200, 1300)
    sleep(5200, 6300)
    while True:
        enterServer = pyautogui.locateCenterOnScreen(
            "./screenshots/enterServer.png",
            confidence=config["confidenceForGFN"],
            region=(885, 801, 160, 55),
        )
        enterGame = pyautogui.locateCenterOnScreen(
            "./screenshots/steamPlay.png", confidence=0.75
        )
        if enterServer != None:
            print("clicking enterServer")
            sleep(1000, 1200)
            # click first server
            pydirectinput.moveTo(x=855, y=582)
            sleep(1200, 1300)
            pydirectinput.click(x=855, y=582, button="left")
            sleep(1000, 1200)
            x, y = enterServer
            pydirectinput.moveTo(x=x, y=y)
            sleep(1200, 1300)
            pydirectinput.click(x=x, y=y, button="left")
            break
        elif enterGame != None:
            print("clicking enterGame")
            x, y = enterGame
            pydirectinput.moveTo(x=x, y=y)
            sleep(200, 300)
            pydirectinput.click(x=x, y=y, button="left")
            sleep(4200, 5300)
            continue
    sleep(3200, 4300)
    while True:
        enterCharacter = pyautogui.locateCenterOnScreen(
            "./screenshots/enterCharacter.png",
            confidence=0.75,
            region=(745, 854, 400, 80),
        )
        if enterCharacter != None:
            sleep(1000, 1200)
            # 点第一页
            sleep(4000, 5000)
            pydirectinput.moveTo(x=138, y=895)
            sleep(500, 600)
            pydirectinput.click(button="left")
            sleep(500, 600)
            pydirectinput.click(button="left")
            sleep(500, 600)
            pydirectinput.click(button="left")
            sleep(500, 600)

            # 点main角色
            sleep(4000, 5000)
            print("clicking mainCharacter")
            pydirectinput.moveTo(
                x=config["charPositionsAtCharSelect"][config["mainCharacter"]][0],
                y=config["charPositionsAtCharSelect"][config["mainCharacter"]][1],
            )
            sleep(500, 600)
            pydirectinput.click(button="left")
            sleep(500, 600)
            pydirectinput.click(button="left")
            sleep(500, 600)
            pydirectinput.click(button="left")
            sleep(500, 600)

            print("clicking enterCharacter")
            x, y = enterCharacter
            pydirectinput.moveTo(x=x, y=y)
            sleep(200, 300)
            pydirectinput.click(x=x, y=y, button="left")
            break
        sleep(2200, 3300)
    states["gameRestartCount"] = states["gameRestartCount"] + 1
    pydirectinput.moveTo(x=config["screenCenterX"], y=config["screenCenterY"])
    sleep(22200, 23300)


def switchToCharacter(index):
    sleep(1500, 1600)
    print("switching to {}".format(index))
    pydirectinput.press("esc")
    sleep(1500, 1600)
    pydirectinput.moveTo(x=config["charSwitchX"], y=config["charSwitchY"])
    sleep(500, 600)
    pydirectinput.click(button="left")
    sleep(200, 300)
    pydirectinput.click(button="left")
    sleep(500, 600)

    pydirectinput.moveTo(
        x=config["charPositions"][index][0], y=config["charPositions"][index][1]
    )
    sleep(500, 600)
    pyautogui.scroll(5)  # fix character switch if you have more then 9 characters
    sleep(500, 600)
    pydirectinput.click(button="left")
    sleep(200, 300)
    pydirectinput.click(button="left")
    sleep(500, 600)

    pydirectinput.moveTo(x=config["charSelectConnectX"], y=config["charSelectConnectY"])
    sleep(500, 600)
    pydirectinput.click(button="left")
    sleep(200, 300)
    pydirectinput.click(button="left")
    sleep(200, 300)
    pydirectinput.click(button="left")
    sleep(1000, 1000)

    pydirectinput.moveTo(x=config["charSelectOkX"], y=config["charSelectOkY"])
    sleep(500, 600)
    pydirectinput.click(button="left")
    sleep(200, 300)
    pydirectinput.click(button="left")
    sleep(200, 300)
    pydirectinput.click(button="left")
    sleep(200, 300)

    states["currentCharacter"] = index
    sleep(10000, 12000)
    if config["GFM"] == True:
        sleep(10000, 12000)


def doGuildDonation():
    pydirectinput.keyDown("alt")
    sleep(100, 200)
    pydirectinput.press("u")
    sleep(100, 200)
    pydirectinput.keyUp("alt")
    sleep(3100, 4200)

    ok = pyautogui.locateCenterOnScreen(
        "./screenshots/ok.png", region=config["regions"]["center"], confidence=0.75
    )

    if ok != None:
        x, y = ok
        pydirectinput.moveTo(x=x, y=y)
        sleep(300, 400)
        pydirectinput.click(x=x, y=y, button="left")
    sleep(1500, 1600)

    pydirectinput.moveTo(x=1431, y=843)
    sleep(500, 600)
    pydirectinput.click(button="left")
    sleep(500, 600)

    pydirectinput.moveTo(x=767, y=561)
    sleep(500, 600)
    pydirectinput.click(button="left")
    sleep(500, 600)

    pydirectinput.press("esc")
    sleep(1500, 1600)

    supportResearch = pyautogui.locateCenterOnScreen(
        "./screenshots/supportResearch.png",
        confidence=0.8,
        region=(1255, 210, 250, 600),
    )

    if supportResearch != None:
        x, y = supportResearch
        print("supportResearch")
        pydirectinput.moveTo(x=x, y=y)
        sleep(500, 600)
        pydirectinput.click(button="left")
        sleep(1500, 1600)

        canSupportResearch = pyautogui.locateCenterOnScreen(
            "./screenshots/canSupportResearch.png",
            confidence=0.8,
            region=(735, 376, 450, 350),
        )

        if canSupportResearch != None:
            pydirectinput.moveTo(x=848, y=520)
            sleep(500, 600)
            pydirectinput.click(button="left")
            sleep(500, 600)

            pydirectinput.moveTo(x=921, y=701)
            sleep(500, 600)
            pydirectinput.click(button="left")
            sleep(500, 600)
        else:
            pydirectinput.press("esc")
            sleep(800, 900)

    sleep(800, 900)
    pydirectinput.press("esc")
    sleep(800, 900)


def doRapport():
    sleep(1000, 2000)
    print("doing Rapport")
    if gameCrashCheck():
        return
    if offlineCheck():
        return
    sleep(3500, 4600)
    # dorapport
    bifrostAvailable = bifrostGoTo(2)
    if bifrostAvailable == False:
        return
    if gameCrashCheck():
        return
    if offlineCheck():
        return
    songandemoterapport()


def songandemoterapport():
    print("song and emote for rapport")
    pydirectinput.keyDown("alt")
    sleep(800, 900)
    pydirectinput.press("w")
    sleep(800, 900)
    pydirectinput.keyUp("alt")
    sleep(800, 900)
    spamG(1000)
    sleep(2000, 3000)
    pydirectinput.moveTo(105, 870)
    sleep(200, 300)
    pydirectinput.click(button="left")
    sleep(200, 300)
    pydirectinput.moveTo(1630, 403)
    sleep(300, 600)
    pydirectinput.click(button="left")
    sleep(300, 600)
    pydirectinput.moveTo(1676, 551)
    sleep(300, 400)
    pydirectinput.click(button="left")
    sleep(30000, 31000)  # 1songduration
    pydirectinput.moveTo(105, 870)
    sleep(300, 600)
    pydirectinput.click(button="left")
    sleep(300, 600)
    pydirectinput.moveTo(1676, 452)
    sleep(300, 600)
    pydirectinput.click(button="left")
    sleep(300, 600)
    pydirectinput.moveTo(1676, 551)
    sleep(300, 400)
    pydirectinput.click(button="left")
    sleep(30000, 31000)  # 2songduration
    pydirectinput.moveTo(118, 904)
    sleep(300, 400)
    pydirectinput.click(button="left")
    sleep(300, 400)
    pydirectinput.moveTo(155, 454)
    sleep(300, 400)
    pydirectinput.click(button="left")
    sleep(300, 400)
    pydirectinput.moveTo(203, 595)
    sleep(300, 400)
    pydirectinput.click(button="left")
    sleep(17000, 20000)  # 1emoteduration
    pydirectinput.moveTo(118, 904)
    sleep(300, 400)
    pydirectinput.click(button="left")
    pydirectinput.moveTo(311, 454)
    sleep(300, 400)
    pydirectinput.click(button="left")
    sleep(300, 400)
    pydirectinput.moveTo(203, 595)
    sleep(300, 400)
    pydirectinput.click(button="left")
    sleep(17000, 20000)  # 2emoteduration
    pydirectinput.moveTo(1832, 900)
    sleep(300, 400)
    pydirectinput.click(button="left")


def doLopang():
    sleep(1000, 2000)
    print("accepting lopang daily")
    doDaily = acceptLopangDaily()
    if doDaily == False:
        return
    sleep(500, 600)
    if gameCrashCheck():
        return
    if offlineCheck():
        return

    sleep(3500, 4600)

    # goto lopang island
    bifrostAvailable = bifrostGoTo(0)
    if bifrostAvailable == False:
        return
    if gameCrashCheck():
        return
    if offlineCheck():
        return
    sleep(3500, 4600)
    walkLopang()
    bifrostGoTo(1)
    if gameCrashCheck():
        return
    if offlineCheck():
        return
    spamG(10000)
    bifrostGoTo(3)
    if gameCrashCheck():
        return
    if offlineCheck():
        return
    spamG(10000)
    bifrostGoTo(4)
    if gameCrashCheck():
        return
    if offlineCheck():
        return
    spamG(10000)


def bifrostGoTo(option):
    print("bifrost to: {}".format(option))
    bifrostXY = [
        [1343, 517],
        [1343, 579],
        [1343, 640],
        [1343, 736],
        [1343, 796],
    ]
    pydirectinput.keyDown("alt")
    sleep(300, 400)
    pydirectinput.press("w")
    sleep(300, 400)
    pydirectinput.keyUp("alt")
    sleep(1500, 1600)

    pydirectinput.moveTo(x=bifrostXY[option][0], y=bifrostXY[option][1])
    sleep(500, 600)
    pydirectinput.click(button="left")
    sleep(1500, 1600)

    # potentially unnecessary check
    if checkBlueCrystal():
        pydirectinput.press("esc")
        sleep(1500, 1600)
        pydirectinput.press("esc")
        sleep(1500, 1600)
        return False
    else:
        # ok
        pydirectinput.moveTo(x=918, y=617)
        sleep(1500, 1600)
        pydirectinput.click(button="left")

    sleep(10000, 12000)

    # wait until loaded
    while True:
        if gameCrashCheck():
            return
        if offlineCheck():
            return
        sleep(1000, 1200)
        inTown = pyautogui.locateCenterOnScreen(
            "./screenshots/inTown.png",
            confidence=0.75,
            region=(1870, 133, 25, 30),
        )
        if inTown != None:
            print("city loaded")
            break
        sleep(1400, 1600)
    sleep(3500, 3600)
    if gameCrashCheck():
        return
    if offlineCheck():
        return
    sleep(4000, 5000)


def walkLopang():
    print("walking lopang")
    spamG(1000)
    walkWithAlt(315, 473, 1500)
    walkWithAlt(407, 679, 1300)
    walkWithAlt(584, 258, 1000)
    walkWithAlt(1043, 240, 1200)
    walkWithAlt(1339, 246, 1300)
    walkWithAlt(1223, 406, 800)
    walkWithAlt(1223, 406, 800)
    walkWithAlt(1263, 404, 800)
    spamG(1000)
    walkWithAlt(496, 750, 800)
    walkWithAlt(496, 750, 800)
    walkWithAlt(496, 750, 800)
    walkWithAlt(653, 737, 800)
    walkWithAlt(653, 737, 800)
    walkWithAlt(674, 264, 800)
    walkWithAlt(573, 301, 1200)
    walkWithAlt(820, 240, 800)
    spamG(1000)
    sleep(1000, 2000)


def checkBlueCrystal():
    """
    # blueCrystal = pyautogui.locateCenterOnScreen(
    #     "./screenshots/blueCrystal.png",
    #     confidence=0.75,
    #     region=config["regions"]["center"],
    # )
    """
    silver1k = pyautogui.locateCenterOnScreen(
        "./screenshots/silver1k.png",
        confidence=0.75,
        region=config["regions"]["center"],
    )

    if silver1k != None:
        return False
    else:
        return True


def acceptLopangDaily():
    sleep(500, 600)
    pydirectinput.keyDown("alt")
    sleep(500, 600)
    pydirectinput.press("j")
    sleep(500, 600)
    pydirectinput.keyUp("alt")
    sleep(1900, 2200)

    pydirectinput.moveTo(x=564, y=313)
    sleep(800, 900)
    pydirectinput.click(button="left")
    sleep(800, 900)

    pydirectinput.moveTo(x=528, y=397)
    sleep(800, 900)
    pydirectinput.click(button="left")
    sleep(800, 900)

    sleep(1900, 2200)
    dailyCompleted = pyautogui.locateCenterOnScreen(
        "./screenshots/dailyCompleted.png",
        confidence=0.75,
        region=(1143, 339, 110, 400),
    )

    if dailyCompleted != None:
        pydirectinput.press("esc")
        sleep(1900, 2200)
        return False

    pydirectinput.moveTo(x=1206, y=398)
    sleep(800, 900)
    pydirectinput.click(button="left")
    sleep(800, 900)

    pydirectinput.moveTo(x=1206, y=455)
    sleep(800, 900)
    pydirectinput.click(button="left")
    sleep(800, 900)

    pydirectinput.moveTo(x=1206, y=512)
    sleep(800, 900)
    pydirectinput.click(button="left")

    sleep(1900, 2200)
    pydirectinput.press("esc")
    sleep(1900, 2200)


def walkWithAlt(lopangX, lopangY, milliseconds):
    lopangX = lopangX
    lopangY = lopangY
    pydirectinput.keyDown("alt")
    pydirectinput.moveTo(x=lopangX, y=lopangY)
    sleep(100, 100)
    pydirectinput.click(button=config["move"])
    sleep(milliseconds / 2, milliseconds / 2)
    pydirectinput.keyUp("alt")
    sleep(milliseconds / 2, milliseconds / 2)


def walkPressG(lopangX, lopangY, milliseconds):
    timeCount = milliseconds / 100
    while timeCount != 0:
        lopangX = lopangX
        lopangY = lopangY
        pydirectinput.moveTo(x=lopangX, y=lopangY)
        sleep(100, 100)
        pydirectinput.click(button=config["move"])
        timeCount = timeCount - 1
        if lopangX % 2 == 0:
            pydirectinput.press("g")


def spamG(milliseconds):
    timeCount = milliseconds / 100
    while timeCount != 0:
        pydirectinput.press("g")
        sleep(90, 120)
        timeCount = timeCount - 1


def buyAuctionFirstFav():
    while True:
        # buying first fav item for 2g or under
        gold2 = pyautogui.locateCenterOnScreen(
            "./screenshots/gold2.png", region=(934, 415, 36, 20), confidence=0.9
        )
        gold1 = pyautogui.locateCenterOnScreen(
            "./screenshots/gold1.png", region=(934, 415, 36, 20), confidence=0.9
        )
        if gold2 != None or gold1 != None:
            # click price input
            pydirectinput.moveTo(x=977, y=504)
            sleep(200, 300)
            pydirectinput.click(button="left")
            sleep(300, 400)
            pydirectinput.press("9")
            sleep(110, 120)
            pydirectinput.press("9")
            sleep(110, 120)
            pydirectinput.press("9")
            sleep(110, 120)
            # click buy
            pydirectinput.moveTo(x=956, y=726)
            sleep(200, 300)
            pydirectinput.click(button="left")
            sleep(300, 400)
            # click ok
            pydirectinput.moveTo(x=959, y=562)
            sleep(200, 300)
            pydirectinput.click(button="left")
            sleep(5300, 5400)

            # click mail
            pydirectinput.moveTo(x=304, y=144)
            sleep(200, 300)
            pydirectinput.click(button="left")
            sleep(300, 400)
            # click first mail
            pydirectinput.moveTo(x=212, y=219)
            sleep(200, 300)
            pydirectinput.click(button="left")
            # click accept
            pydirectinput.moveTo(x=440, y=515)
            sleep(200, 300)
            pydirectinput.click(button="left")
            # click delete
            pydirectinput.moveTo(x=518, y=515)
            sleep(200, 300)
            pydirectinput.click(button="left")
            sleep(5300, 5400)
            # click
            pydirectinput.moveTo(x=1320, y=355)
            sleep(200, 300)
            pydirectinput.click(button="left")
            sleep(300, 400)
            # click bottom right buy
            pydirectinput.moveTo(x=1416, y=828)
            sleep(200, 300)
            pydirectinput.click(button="left")
            sleep(300, 400)
        else:
            # click refresh
            pydirectinput.moveTo(x=1062, y=298)
            sleep(200, 300)
            pydirectinput.click(button="left")
            sleep(300, 400)


if __name__ == "__main__":
    states = newStates.copy()
    main()
