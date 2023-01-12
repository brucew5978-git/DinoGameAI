import matplotlib.pyplot as plt
import pyautogui as pg
import time
import keyboard

class CollectorError(Exception):
    pass    

class CircularQueue:

    def __init__(self, length):
        self.length = length
        self.items = [None] * n
        self.size = 0
        self.start = 0

    def enqueue(self, item):
        if self.isFull():
            return False
        
        self.items[self.getEnd()] = item
        self.size+=1

    def dequeue(self):
        if self.isEmpty():
            return False

        dequeueValue = self.items[self.start]
        self.items[self.start]=None
        self.start=(self.start+1) % self.length
        self.size-=1
        return dequeueValue

    def isFull(self):
        return self.size==self.length

    def isEmpty(self):
        return self.size==0

    def getEnd(self):
        return (self.start+self.size)%self.length

    def clear(self):
        self.items=[None]*self.length
        self.size=0
        self.start=0
    

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

class KeyboardDetector:

    def getState(self):
        
        state=''
        if keyboard.is_pressed('up'):
            state+='u'

        if keyboard.is_pressed('down'):
            state+='d'

        return state

class DataCollector:

    def __init__(self, lastImageID=0, detector=KeyboardDetector()):
        #lastImageID == last image saved to a file

        print('[dataCollector.INIT]')
        time.sleep(5)

        dimensions=findScreen()
        self.detector = detector
        self.ID=lastImageID

        self.dimensions = (dimensions['screenLeft'], dimensions['screenTop'], dimensions['screenRight'], dimensions['screenBottom'])
        print(self.dimensions)
    
    def screenshot(self):
        img = pg.screenshot()
        img = img.crop(self.dimensions)
        img=img.resize((238,412))
        return img

    def getGameState(self):
        return self.detector.getState()


class PDataCollector(DataCollector):

    def __init__(self, hotkey='w', lastImageID=0, detector=KeyboardDetector()):
        super(PDataCollector, self).__init__(lastImageID, detector)
        self.isPressed = False
        self.hotkey = hotkey

    def run(self, root='data'):
        if keyboard.is_pressed(self.hotkey) and not self.isPressed:
            self.isPressed = True
            img = self.screenshot()
            imageID='{:06d}'.format(self.ID)
            imageName = f'{root}/images/{imageID}.jpg'

            print(imageName)
            img.save(imageName)
            self.ID+=1
        
        elif not keyboard.is_pressed(self.hotkey):
            self.isPressed = False


#dataCollector = PDataCollector(lastImageID=0, hotkey='w')

keyboard.add_hotkey('a', lambda: keyboard.write('Geek'))
keyboard.add_hotkey('ctrl + shift + a', print, args =('you entered', 'hotkey'))
  
keyboard.wait('esc')

while True:
    '''if keyboard.is_pressed('0x31'):
        print('ending...')
        break
    '''
 
    #dataCollector.run()

#Find screen

#Press key detection function
#File write function for storing screenshots
#Circular queue for storing imgs
#Use circular queue to backtrack where model should jump

