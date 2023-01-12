import matplotlib.pyplot as plt
import pyautogui as pg
import time
from pynput import keyboard

class CollectorError(Exception):
    pass


def findScreen():
    print("In Find Screen")
    targetIcon = pg.locateOnScreen('reference/HighScoreCorner.jpg', confidence=0.9)
    
    bottomCorner = pg.locateOnScreen('reference/NoInternet.jpg', confidence=0.9)
    print(targetIcon)

    if(bottomCorner!=None):
        screenRight, screenTop = (targetIcon.left, targetIcon.top)
        screenLeft, screenBottom = (bottomCorner.left, bottomCorner.top)

        windowWidth = screenRight-screenLeft
        windowHeight = screenBottom-screenTop

        #img = pg.screenshot(region=(screenLeft, screenTop, windowWidth, windowHeight))
        #img.save("data/newScreenShot.png")

        print(f"[FIND_SCREEN] {screenRight-screenLeft}W x {screenBottom-screenTop}H")
        return {'screenLeft': screenLeft, 'screenRight': screenRight, 'screenBottom': screenBottom, 'screenTop': screenTop}

    raise CollectorError('Screen not found...')

def frequencyPhotoTaker():
    return 0

def on_press(key):
    try:

        if(key.char == "w"):
            print("Jump detected")



    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

#dataCollector = PDataCollector(lastImageID=0, hotkey='w')

'''
while True:
   if keyboard.is_pressed('0x31'):
        print('ending...')
        break
    '''
 
    #dataCollector.run()

#Find screen
#Press key detection function and takes a photo
#Periodic photo taker

#File write function for going through data and creating csv for sorting