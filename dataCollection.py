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
    targetIcon = pg.locateOnScreen('reference/targetDinoGameIcon.png', confidence=0.9)
    
    bottomCorner = pg.locateOnScreen('reference/BottomScreenCorner.jpeg', confidence=0.9)

    if(targetIcon!=None and bottomCorner!=None):
        screenLeft, screenTop = (targetIcon.left, targetIcon.top)
        screenRight, screenBottom = (bottomCorner.left+bottomCorner.width, bottomCorner.top+bottomCorner.height)

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
        print(dimensions)
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


dataCollector = PDataCollector(lastImageID=0, hotkey='w')
while True:
    if keyboard.is_pressed('p'):
        print('ending...')
        break
    dataCollector.run()

'''
class PassiveDataCollector(DataCollector):

    def __init__(self, sleepTime=0.1, queueSize=8, lastImageID=0, detector=KeyboardDetector()):
        super(PassiveDataCollector, self).__init__(lastImageID, detector)

        self.queue=CircularQueue(queueSize)
        self.sleepTime=sleepTime
        self.lastTime=-1

    def run(self, root='data'):
        state=self.getGameState()

        if (len(state) ==0 and time.time()-self.lastTime >= self.sleepTime*10):
            img = self.screenshot()
            self.queue.enqueue(img)
            self.lastTime=time.time()

        elif(len(state)!=0):
            print('Clearing queue')

            self.queue.clear()
            time.sleep(3 * self.sleepTime)
            self.lastTime=time.time()

        if self.queue.isFull():
            img=self.queue.dequeue()
            self.queue.clear()

            imageID='{:06d}'.format(self.ID)
            imageName = f'{root}/images/{imageID}.jpg'

            print(imageName)
            img.save(imageName)
            self.ID+=1
'''
