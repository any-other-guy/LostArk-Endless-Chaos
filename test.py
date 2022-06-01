
import pyautogui

while True:
    # print(pyautogui.locateOnScreen('./screenshots/portal.png', grayscale = True, confidence = 0.75, region=(1652, 168, 240, 210)))
    # print(pyautogui.locateOnScreen('./screenshots/selfPixel.png', region=(1652, 168, 240, 210)))
    print(pyautogui.displayMousePosition())
    # im = pyautogui.screenshot(region=(1652, 168, 240, 210))
    # print(im.getpixel((1772 - 1652,272 - 168)))
    # minimap = pyautogui.screenshot(region=(1652, 168, 240, 210)) #Top Right
    # width, height = minimap.size
    # for x in range(0, width):
    #     for y in range(0, height):
    #         r, g, b = minimap.getpixel((x,y))
    #         print("x: {} y: {} r: {} g: {} b: {}".format(x, y, r, g, b))
    #         if (r > 120 g > 100 and b < 60):
    #             left, top,_w, _h = tuple(1652, 168, 240, 210)
    #             xx = left + x;
    #             yy = top + y;
    #             print("floor2BossX: {} floor2BossY: {}".format(xx, yy))
                