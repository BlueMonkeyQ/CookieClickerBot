import cv2
import numpy as np
import pyscreeze
import pyautogui
import time
import schedule
import subprocess
import os
from PIL import ImageGrab
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pathlib import Path

base_dir = Path(__file__).resolve().parent
screenshotsDir = base_dir / "screenshots"
bigCookieFilepath = screenshotsDir / "bigCookie.png"
storeFilepath =  screenshotsDir / "store.png"
optionsFilepath = screenshotsDir / "options.png"
fullscreenOffFilepath = screenshotsDir / "fullscreenoff.png"
fullscreenOnFilepath = screenshotsDir / "fullscreenon.png"
screen = ImageGrab.grab()
screen_width, screen_height = screen.size

def launchGame():
    # Get game filepath
    # If txt file does not exist, prompt user to get it

    if os.path.exists(Path(r"gameFilePath.txt")) is False or os.stat(Path(r"gameFilePath.txt")).st_size == 0:
        Tk().withdraw()
        filepath = askopenfilename()
        with open(Path(r"gameFilePath.txt"), 'w') as f:
            f.write(filepath)

    else:
        with open(Path(r"gameFilePath.txt"), 'r') as f:
            filepath = f.read()

    try:
        subprocess.Popen(filepath)
    except Exception as e:
        print(e)

    # let game load
    time.sleep(5)
    
    # Set game to fullscreen
    findImage(optionsFilepath)
    pyautogui.click()
    if findImage(fullscreenOnFilepath,0.9) is False:
        findImage(fullscreenOffFilepath,0.8)
        pyautogui.click()
        time.sleep(1)

    findImage(optionsFilepath)
    pyautogui.click()

def saveGame():
    pyautogui.hotkey('ctrl','s')

def findImage(filepath: Path, threshold:float = 0.0):
    screenshot = pyscreeze.screenshot()
    screenshot = np.array(screenshot)
    screenshot_grey_scale = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    target_image = cv2.imread(filepath,cv2.IMREAD_GRAYSCALE)
    # Perform template matching
    result = cv2.matchTemplate(screenshot_grey_scale, target_image, cv2.TM_CCOEFF_NORMED)
    
    # Get the location of the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # Get the dimensions of the target image
    target_w, target_h = target_image.shape[::-1]
    
    if max_val >= threshold:
        # Calculate the center of the found target
        center_x = max_loc[0] + target_w // 2
        center_y = max_loc[1] + target_h // 2
        pyautogui.moveTo(center_x, center_y)
        pyautogui.moveTo(center_x, center_y)
        return True
    else:
        return False

def findUpgrades():
    screenshot = pyscreeze.screenshot()
    screenshot = np.array(screenshot)

    green_pixels = np.where(
        (screenshot[:, :, 1] > 200) &      # Green channel is high
        (screenshot[:, :, 0] < 100) &      # Red channel is low
        (screenshot[:, :, 2] < 100)        # Blue channel is low
    )

    if len(green_pixels[0]) > 0:
        print("Upgrade Found")
        y,x = green_pixels[0][0], green_pixels[1][0]
        pyautogui.moveTo(x,y)
        pyautogui.click()
        findImage(bigCookieFilepath)
    else:
        print("No Upgrade Found")

def findClickerUpgrades():
    findImage(storeFilepath)
    pyautogui.moveRel(screen_width*-0.05,screen_height*0.03)
    pyautogui.tripleClick()
    findImage(bigCookieFilepath)

launchGame()
findClickerUpgrades()

schedule.every(1).seconds.do(findUpgrades)
schedule.every(5).seconds.do(saveGame)
schedule.every(10).seconds.do(findClickerUpgrades)

findImage(bigCookieFilepath)

while True:
    schedule.run_pending()
    pyautogui.tripleClick()