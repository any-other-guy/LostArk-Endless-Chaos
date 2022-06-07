from config import config
import pyautogui
import time
import random
import math

newStates = {
    "status": "inCity",
    "abilityScreenshots": [],
    "clearCount": 0,
    "moveToX": None,
    "moveToY": None,
    "instanceStartTime": None,
    "deathCount": 0,
    "healthPotCount": 0,
}
states = newStates.copy()


def main():
    print("Endless Chaos started...")
    while True:
        if states["status"] == "inCity":
            # states = newStates
            states["abilityScreenshots"] = []
            enterChaos()
        elif states["status"] == "floor1":
            # wait for loading
            waitForLoading()
            sleep(1000, 1200)
            print("floor1 loaded")

            # saving clean abilities icons
            saveAbilitiesScreenshots()

            # check repair
            if config["autoRepair"]:
                doRepair()

            # save instance start time
            states["instanceStartTime"] = int(time.time_ns() / 1000000)

            # do floor one
            doFloor1()
        elif states["status"] == "floor2":
            # wait for loading
            waitForLoading()
            print("floor2 loaded")
            # do floor two
            doFloor2()


def enterChaos():
    rightClick = "right"
    # if config["move"] == "right":
    #     rightClick = "left"

    pyautogui.click(
        x=config["screenCenterX"], y=config["screenCenterY"], button=rightClick
    )
    sleep(500, 800)

    while True:
        enterHand = pyautogui.locateOnScreen("./screenshots/enterChaos.png")
        if enterHand != None:
            print("entering chaos...")
            pyautogui.press(config["interact"])
            break
        sleep(500, 800)
    # while True:
    #     im = pyautogui.screenshot(region=(1652, 168, 240, 210))
    #     r, g, b = im.getpixel((1772 - 1652, 272 - 168))
    #     if r != 0 and g != 0 and b != 0:
    #         break
    # sleep(500, 800)
    # pyautogui.keyDown("alt")
    # sleep(200, 300)
    # pyautogui.press("q")
    # sleep(200, 300)
    # pyautogui.keyUp("alt")
    # sleep(800, 1000)
    # pyautogui.moveTo(886, 346)
    # sleep(800, 1000)
    # pyautogui.click(1182, 654, button="left")
    # sleep(800, 1000)
    # pyautogui.click(1182, 654, button="left")
    while True:
        enterButton = pyautogui.locateCenterOnScreen(
            "./screenshots/enterButton.png", confidence=0.75
        )
        if enterButton != None:
            x, y = enterButton
            pyautogui.moveTo(x=x, y=y)
            sleep(500, 800)
            pyautogui.click(x=x, y=y, button="left")
            break
    sleep(500, 800)
    while True:
        acceptButton = pyautogui.locateCenterOnScreen(
            "./screenshots/acceptButton.png", confidence=0.75
        )
        if acceptButton != None:
            x, y = acceptButton
            pyautogui.moveTo(x=x, y=y)
            sleep(500, 800)
            pyautogui.click(x=x, y=y, button="left")
            break
    states["status"] = "floor1"
    return


def doFloor1():
    # trigger start floor 1
    pyautogui.click(x=945, y=550, button=config["move"])
    # delayed start for better aoe abiltiy usage at floor1 beginning
    if config["delayedStart"] != None:
        sleep(config["delayedStart"] - 100, config["delayedStart"] + 100)

    # # move to a side
    # pyautogui.press(config["blink"])
    # sleep(400, 500)

    # pyautogui.mouseDown(random.randint(800, 1120), random.randint(540, 580), button=config['move'])
    # sleep(2000,2200)
    # pyautogui.click(x=960, y=530, button=config['move'])

    # smash available abilities
    useAbilities()
    # bad run quit
    if checkTimeout():
        quitChaos()
        return
    calculateMinimapRelative(states["moveToX"], states["moveToY"])
    enterPortal()
    states["status"] = "floor2"
    return


def doFloor2():
    pyautogui.mouseDown(x=1150, y=500, button=config["move"])
    sleep(800, 900)
    pyautogui.mouseDown(x=960, y=200, button=config["move"])
    sleep(800, 900)
    pyautogui.click(x=945, y=550, button=config["move"])

    useAbilities()
    # bad run quit
    if checkTimeout():
        quitChaos()
        return

    # quit chaos after floor 2 clera for now
    quitChaos()

    # TODO: going floor 3 here
    # print('floor 2 clear')
    # calculateMinimapRelative(states['moveToX'], states['moveToY'])
    # enterPortal()
    # states['status'] = 'floor3'

    return


def quitChaos():
    # quit
    print("quitting")
    while True:
        leaveButton = pyautogui.locateCenterOnScreen(
            "./screenshots/leave.png",
            confidence=0.75,
            region=config["regions"]["leaveMenu"],
        )
        if leaveButton != None:
            x, y = leaveButton
            # pyautogui.moveTo(x=x, y=y)
            # sleep(500,600)
            while (
                pyautogui.locateCenterOnScreen("./screenshots/ok.png", confidence=0.75)
                == None
            ):
                pyautogui.moveTo(x=x, y=y)
                sleep(500, 600)
                pyautogui.click(button="left")
                sleep(150, 200)
            break
        break
    sleep(500, 600)
    while True:
        okButton = pyautogui.locateCenterOnScreen(
            "./screenshots/ok.png", confidence=0.75
        )
        if okButton != None:
            x, y = okButton
            pyautogui.moveTo(x=x, y=y)
            sleep(500, 600)
            # pyautogui.click(x=x, y=y, button='left')
            pyautogui.click(button="left")
            break
        sleep(500, 600)
    states["status"] = "inCity"
    states["clearCount"] = states["clearCount"] + 1
    lastRun = str((int(time.time_ns() / 1000000) - states["instanceStartTime"]) / 1000)
    print(
        "Total runs completed: {}, total death: {}, last run: {}s".format(
            states["clearCount"], states["deathCount"], lastRun
        )
    )
    return


def useAbilities():
    while True:
        diedCheck()
        healthCheck()
        if checkTimeout():
            return
        # check boss
        if states["status"] == "floor2" and checkFloor2Boss():
            calculateMinimapRelative(states["moveToX"], states["moveToY"])
            moveToMinimapRelative(
                states["moveToX"], states["moveToY"], 1000, 1100, True
            )
            fightFloor2Boss()
        # check elite and mobs
        if states["status"] == "floor2" and checkFloor2Elite():
            calculateMinimapRelative(states["moveToX"], states["moveToY"])
            moveToMinimapRelative(states["moveToX"], states["moveToY"], 800, 900, True)
        elif states["status"] == "floor2" and checkFloor2Mob():
            calculateMinimapRelative(states["moveToX"], states["moveToY"])
            moveToMinimapRelative(states["moveToX"], states["moveToY"], 400, 500, False)

        # cast
        for i in range(0, len(states["abilityScreenshots"])):
            # pyautogui.moveTo(x=960, y=540)
            diedCheck()
            healthCheck()
            # check portal 防止直接打死boss不小心
            if states["status"] == "floor2" and checkPortal():
                return

            # check portal
            if states["status"] == "floor1" and checkPortal():
                return

            # cast spells
            pyautogui.moveTo(x=config["screenCenterX"], y=config["screenCenterY"])
            checkCDandCast(states["abilityScreenshots"][i])


def checkCDandCast(ability):
    if pyautogui.locateOnScreen(
        ability["image"], region=config["regions"]["abilities"]
    ):
        if ability["cast"]:
            start_ms = int(time.time_ns() / 1000000)
            now_ms = int(time.time_ns() / 1000000)
            # spam until cast time before checking cd, to prevent 击倒后情况
            while now_ms - start_ms < ability["castTime"]:
                pyautogui.press(ability["key"])
                now_ms = int(time.time_ns() / 1000000)
            while pyautogui.locateOnScreen(
                ability["image"], region=config["regions"]["abilities"]
            ):
                pyautogui.press(ability["key"])
        elif ability["hold"]:
            start_ms = int(time.time_ns() / 1000000)
            now_ms = int(time.time_ns() / 1000000)
            # spam until cast time before checking cd, to prevent 击倒后情况
            while now_ms - start_ms < ability["holdTime"]:
                pyautogui.keyDown(ability["key"])
                now_ms = int(time.time_ns() / 1000000)
            while pyautogui.locateOnScreen(
                ability["image"], region=config["regions"]["abilities"]
            ):
                pyautogui.keyDown(ability["key"])
        else:
            # 瞬发 ability
            pyautogui.press(ability["key"])
            while pyautogui.locateOnScreen(
                ability["image"], region=config["regions"]["abilities"]
            ):
                pyautogui.press(ability["key"])


def checkPortal():
    # check portal image
    portal = pyautogui.locateCenterOnScreen(
        "./screenshots/portal.png", region=config["regions"]["minimap"], confidence=0.7
    )
    if portal != None:
        x, y = portal
        states["moveToX"] = x
        states["moveToY"] = y
        print("portal image x: {} y: {}".format(states["moveToX"], states["moveToY"]))
        return True

    # check pixel
    minimap = pyautogui.screenshot(region=config["regions"]["minimap"])  # Top Right
    width, height = minimap.size
    order = spiralSearch(width, height, math.floor(width / 2), math.floor(height / 2))
    for entry in order:
        if entry[1] >= width or entry[0] >= height:
            continue
        r, g, b = minimap.getpixel((entry[1], entry[0]))

        # if (b > 250 and g >130 and g < 150 and r > 60 and r < 85) or (b > 250 and g > 180 and r >100 and r < 120):
        # if(r == 80, g == 146, b == 255) or (r == 126, g ==  214, b == 255):
        if (r in range(75, 85) and g in range(140, 150) and b in range(250, 255)) or (
            r in range(120, 130) and g in range(210, 220) and b in range(250, 255)
        ):
            left, top, _w, _h = config["regions"]["minimap"]
            states["moveToX"] = left + entry[1]
            states["moveToY"] = top + entry[0]
            print(
                "portal pixel x: {} y: {}, r: {} g: {} b: {}".format(
                    states["moveToX"], states["moveToY"], r, g, b
                )
            )
            return True
    return False


def checkFloor2Elite():
    sleep(100, 200)
    minimap = pyautogui.screenshot(region=config["regions"]["minimap"])  # Top Right
    width, height = minimap.size
    order = spiralSearch(width, height, math.floor(width / 2), math.floor(height / 2))
    for entry in order:
        if entry[1] >= width or entry[0] >= height:
            continue
        r, g, b = minimap.getpixel((entry[1], entry[0]))
        if (
            (r in range(200, 215)) and (g in range(125, 150)) and (b in range(30, 60))
        ):  # (r > 120 and r < 160 and g < 85 and g > 60 and b < 20) or (r > 190 and g > 130 and g < 150 and b > 30 and b < 60)
            left, top, _w, _h = config["regions"]["minimap"]
            states["moveToX"] = left + entry[1]
            states["moveToY"] = top + entry[0]
            print(
                "elite x: {} y: {}, r: {} g: {} b: {}".format(
                    states["moveToX"], states["moveToY"], r, g, b
                )
            )
            return True


def checkFloor2Mob():
    sleep(100, 200)
    minimap = pyautogui.screenshot(region=config["regions"]["minimap"])  # Top Right
    width, height = minimap.size
    order = spiralSearch(width, height, math.floor(width / 2), math.floor(height / 2))
    for entry in order:
        if entry[1] >= width or entry[0] >= height:
            continue
        r, g, b = minimap.getpixel((entry[1], entry[0]))
        if r == 208 and g == 24 and b == 24:  # r == 199 and g == 28 and b == 30
            left, top, _w, _h = config["regions"]["minimap"]
            states["moveToX"] = left + entry[1]
            states["moveToY"] = top + entry[0]
            print(
                "mob x: {} y: {}, r: {} g: {} b: {}".format(
                    states["moveToX"], states["moveToY"], r, g, b
                )
            )
            return True


def checkFloor2Boss():
    fightFloor2Boss()
    bossLocation = pyautogui.locateCenterOnScreen(
        "./screenshots/boss.png", confidence=0.65
    )
    if bossLocation != None:
        bossLocation = tuple(bossLocation)
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


def fightFloor2Boss():
    if pyautogui.locateOnScreen("./screenshots/bossBar.png", confidence=0.75):
        print("boss bar located")
        sleep(500, 700)
        # pyautogui.press("z")
        # sleep(1000, 1100)
        pyautogui.press("V")
        sleep(1000, 1100)


def calculateMinimapRelative(x, y):
    selfLeft = config["minimapCenterX"]
    selfTop = config["minimapCenterY"]
    if abs(selfLeft - x) <= 11 and abs(selfTop - y) <= 11:
        states["moveToX"] = config["screenCenterX"]
        states["moveToY"] = config["screenCenterY"]
        return

    x = x - selfLeft
    y = y - selfTop
    print("relative to center pos x: {} y: {}".format(x, y))

    dist = 200
    if y < 0:
        dist = -dist

    if x == 0:
        if y < 0:
            newY = y - abs(dist)
        else:
            newY = y + abs(dist)
        print("relative to center pos newX: 0 newY: {}".format(int(newY)))
        states["moveToX"] = 0 + config["screenCenterX"]
        states["moveToY"] = int(newY) + config["screenCenterY"]
        return
    if y == 0:
        if x < 0:
            newX = x - abs(dist)
        else:
            newX = x + abs(dist)
        print("relative to center pos newX: {} newY: 0".format(int(newX)))
        states["moveToX"] = int(newX) + config["screenCenterX"]
        states["moveToY"] = 0 + config["screenCenterY"]
        return

    k = y / x
    # newX = x + dist
    newY = y + dist
    # newY = k * (newX - x) + y
    newX = (newY - y) / k + x

    print("before confining newX: {} newY: {}".format(int(newX), int(newY)))
    if newX < 0 and abs(newX) > config["clickableAreaX"]:
        newX = -config["clickableAreaX"]
        if newY < 0:
            newY = newY + abs(dist) * 0.9
        else:
            newY = newY - abs(dist) * 0.9
    elif newX > 0 and abs(newX) > config["clickableAreaX"]:
        newX = config["clickableAreaX"]
        if newY < 0:
            newY = newY + abs(dist) * 0.9
        else:
            newY = newY - abs(dist) * 0.9

    if newY < 0 and abs(newY) > config["clickableAreaY"]:
        newY = -config["clickableAreaY"]
        if newX < 0:
            newX = newX + abs(dist) * 0.9
        else:
            newX = newX - abs(dist) * 0.9
    elif newY > 0 and abs(newY) > config["clickableAreaY"]:
        newY = config["clickableAreaY"]
        if newX < 0:
            newX = newX + abs(dist) * 0.9
        else:
            newX = newX - abs(dist) * 0.9

    print(
        "after confining relative to center pos newX: {} newY: {}".format(
            int(newX), int(newY)
        )
    )
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

    # moving in a straight line
    pyautogui.click(x=x, y=y, button=config["move"])
    sleep(int(timeMin / 2), int(timeMax / 2))
    pyautogui.click(x=x, y=y, button=config["move"])
    sleep(int(timeMin / 2), int(timeMax / 2))
    # sleep(timeMin, timeMax)

    # optional blink here
    if blink:
        pyautogui.press(config["blink"])
        sleep(300, 400)

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
    #     pyautogui.mouseDown(x=x, y=y, button=config['move'])
    #     sleep(math.floor(timeMin / 3), math.floor(timeMax / 3))
    #     turn = not turn
    #     count = count + 1


def enterPortal():
    # repeatedly move and press g until black screen
    sleep(2200, 2500)
    print("moving to portal x: {} y: {}".format(states["moveToX"], states["moveToY"]))
    while True:
        im = pyautogui.screenshot(region=(1652, 168, 240, 210))
        r, g, b = im.getpixel((1772 - 1652, 272 - 168))
        if r == 0 and g == 0 and b == 0:
            return

        if (
            states["moveToX"] == config["screenCenterX"]
            and states["moveToY"] == config["screenCenterY"]
        ):
            pyautogui.press(config["interact"])
            sleep(100, 120)
        else:
            pyautogui.mouseDown(
                x=states["moveToX"], y=states["moveToY"], button=config["move"]
            )
            sleep(100, 120)
            pyautogui.press(config["interact"])


# def enterPortal():
#     # repeatedly move and press g until black screen
#     print('moving to portal x: {} y: {}'.format(states['moveToX'], states['moveToY']))
#     turn = True
#     deflect = 60
#     while True:
#         im = pyautogui.screenshot(region=(1652, 168, 240, 210))
#         r,g,b = im.getpixel((1772 - 1652,272 - 168))
#         if r == 0 and g == 0 and b == 0:
#             return

#         x = states['moveToX']
#         y = states['moveToY']
#         if x > 960 and y < 540:
#             if turn:
#                 x = x - deflect* 2.5
#                 y = y - deflect
#             else:
#                 x = x + deflect* 2.5
#                 y = y + deflect
#         elif x > 960 and y > 540:
#             if turn:
#                 x = x + deflect* 2.5
#                 y = y - deflect
#             else:
#                 x = x - deflect * 2.5
#                 y = y + deflect
#         elif x < 960 and y > 540:
#             if turn:
#                 x = x + deflect* 2.5
#                 y = y + deflect
#             else:
#                 x = x - deflect* 2.5
#                 y = y - deflect
#         elif x < 960 and y < 540:
#             if turn:
#                 x = x - deflect* 2.5
#                 y = y + deflect
#             else:
#                 x = x + deflect* 2.5
#                 y = y - deflect
#         # print('movex: {} movey: {} x:{} y: {} turn: {}'.format(states['moveToX'], states['moveToY'], x,y,turn))
#         count = 0
#         while count < 5:
#             pyautogui.press(config['interact'])
#             im = pyautogui.screenshot(region=(1652, 168, 240, 210))
#             r,g,b = im.getpixel((1772 - 1652,272 - 168))
#             if r == 0 and g == 0 and b == 0:
#                 return

#             pyautogui.click(x=x, y=y, button=config['move'])
#             sleep(50,60)
#             count = count + 1
#         turn = not turn
#     return


def waitForLoading():
    print("loading")
    while True:
        if pyautogui.locateOnScreen(
            "./screenshots/leave.png",
            confidence=0.8,
            region=config["regions"]["leaveMenu"],
        ):
            return True
        sleep(222, 333)


def saveAbilitiesScreenshots():
    for ability in config["abilities"]:
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
            }
        )
    # print(states['abilityScreenshots'])


def diedCheck():  # get information about wait a few second to revive
    if pyautogui.locateOnScreen(
        "./screenshots/died.png", grayscale=True, confidence=0.9
    ):
        states["deathCount"] = states["deathCount"] + 1
        sleep(5000, 5500)
        while (
            pyautogui.locateOnScreen("./screenshots/resReady.png", confidence=0.7)
            != None
        ):
            pyautogui.moveTo(1275, 454)
            sleep(600, 800)
            pyautogui.click(1275, 454, button="left")
            sleep(600, 800)
            pyautogui.moveTo(config["screenCenterX"], config["screenCenterY"])
    return


def doRepair():
    # Check if repair needed
    # if pyautogui.locateOnScreen("./screenshots/repair.png", grayscale = True, confidence = 0.8):
    pyautogui.keyDown("alt")
    sleep(200, 300)
    pyautogui.press("p")
    sleep(200, 300)
    pyautogui.keyUp("alt")
    sleep(800, 1000)
    pyautogui.moveTo(1182, 654)
    sleep(800, 1000)
    pyautogui.click(1182, 654, button="left")
    sleep(800, 1000)
    pyautogui.moveTo(1068, 644)
    sleep(800, 1000)
    pyautogui.click(1068, 644, button="left")
    sleep(800, 1000)
    pyautogui.press("esc")
    sleep(800, 1000)
    pyautogui.press("esc")
    sleep(800, 1000)


def healthCheck():
    r, g, b = pyautogui.pixel(config["healthCheckX"], config["healthCheckY"])
    if r < 20 and config["useHealthPot"]:
        pyautogui.press(config["healthPot"])
        states["healthPotCount"] = states["healthPotCount"] + 1
        return
    return


def sleep(min, max):
    time.sleep(random.randint(min, max) / 1000.0)


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
    if currentTime - states["instanceStartTime"] > config["timeLimit"]:
        print("timeout triggered")
        timeout = pyautogui.screenshot()
        timeout.save("./timeout/timeout" + str(currentTime) + ".png")
        return True
    return False


if __name__ == "__main__":
    main()
