import os
import pandas as pd
from torch.utils.data import Dataset
from torchvision import transforms
import torch
from PIL import Image

def renameByIndices(baseFolder='data', graph=False):
    
    totalImages=0
    folders = []
    numbers = []

    for root, subfolder, path in os.walk(baseFolder):
        root = root.replace('\\', '/')
        if not subfolder:
            subfolder = ['']
        for folder in subfolder:
            
            imageID = 0

            if folder != '':
                folder+='/'

            for f in sorted(path):
                oldPath = root + '/' + folder + f
                newPath = root + '/' + folder + '{:06d}'.format(imageID) + '.jpg'
                os.rename(oldPath, newPath)
                imageID+=1

            if imageID > 0:
                print(root + '/' + folder)
                print(imageID)

                folders.append(root + '/' + folder)
                numbers.append(imageID)
                totalImages+=imageID
    
    print('total: ', totalImages)
    return totalImages

def makeSpreadsheet(outPath='images.csv', baseFolder='data'):

    labels = {
        f'{baseFolder}'/
    }
