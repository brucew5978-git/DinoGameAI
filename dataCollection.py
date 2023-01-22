import pyautogui as pg
import time
from pynput import keyboard

currentJumpTime = time.time()

class CollectorError(Exception):
    pass

class CircularQueue:

    def __init__(self, n):
        self.n = n
        self.items = [None] * n
        self.size = 0
        self.start = 0

    def enqueue(self, item):
        if self.is_full():
            self.dequeue()
        self.items[self.get_end()] = item
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            return
        tmp = self.items[self.start]
        self.items[self.start] = None
        self.start = (self.start + 1) % self.n
        self.size -= 1
        return tmp

    def is_full(self):
        return self.size == self.n

    def is_empty(self):
        return self.size == 0

    def get_end(self):
        return (self.start + self.size) % self.n

    def clear(self):
        self.items = [None] * self.n
        self.size = 0
        self.start = 0

def findScreen():
    print("In Find Screen")
    targetIcon = pg.locateOnScreen('reference/HighScoreCorner.jpg', confidence=0.9)
    
    bottomCorner = pg.locateOnScreen('reference/NoInternet.jpg', confidence=0.9)
    print(targetIcon)
    if(bottomCorner!=None):
        screenRight, screenTop = (targetIcon.left, targetIcon.top)
        screenLeft, screenBottom = (bottomCorner.left, bottomCorner.top)

        print(f"[FIND_SCREEN] {screenRight-screenLeft}W x {screenBottom-screenTop}H")
        return screenLeft, screenRight, screenBottom, screenTop

    raise CollectorError('Screen not found...')


def onPress(key):
    try:
        if(key == keyboard.Key.space):
            print("Jump detected")
            global currentJumpTime
            currentJumpTime = time.time()

            #newCapture = pg.screenshot(region=(SCREEN_LEFT, SCREEN_TOP, SCREEN_WIDTH, SCREEN_HEIGHT))
            newCapture = imageQueue.dequeue()
            rootName = f"data/1/jump_{currentJumpTime}.png"
            newCapture.save(rootName)
            
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def onRelease(key):
    if(key == keyboard.Key.esc):
        # Stop listener
        return False


class Data_Collector():
    def __init__(self):
        self.left, self.right, self.bottom, self.top = findScreen()

        global SCREEN_TOP, SCREEN_LEFT, SCREEN_WIDTH, SCREEN_HEIGHT
        SCREEN_TOP, SCREEN_LEFT = self.top, self.left
        
        print(self.left)
        print(self.right)

        self.width = self.right-self.left
        self.height = self.bottom-self.top

        SCREEN_WIDTH = self.width
        SCREEN_HEIGHT = self.height

        global currentJumpTime

        self.time = time.time()
        self.jumpTime = currentJumpTime

        queueSize = 2
        global imageQueue
        imageQueue = CircularQueue(queueSize)

    def takeImg(self):
        self.time = time.time()
        self.jumpTime = currentJumpTime

        image = pg.screenshot(region=(self.left, self.top, self.width, self.height))
        imageQueue.enqueue(image)
        
        #rootName = f"data/test_{self.time}.png"
        #image.save(rootName)  
        
        if(self.time - self.jumpTime > 0.45):        
            rootName = f"data/0/normal_{self.time}.png"
            image.save(rootName)   

            
 

if __name__ == "__main__":
    newData = Data_Collector()

    # Collect events until released

    # ...or, in a non-blocking fashion:
    listener = keyboard.Listener(on_press=onPress, on_release=onRelease)
    listener.start()
    #dataCollector = PDataCollector(lastImageID=0, hotkey='w')

    print("Data Recording Start")
    time.sleep(3.5)

    while True:
    #for i in range(5):
        time.sleep(0.8)
        newData.takeImg()
  

    #dataCollector.run()

    #Find screen
    #Press key detection function and takes a photo
    #Periodic photo taker
    #Can wrap all 3 functionalities into a class for easier use

    #File write function for going through data and creating csv for sorting