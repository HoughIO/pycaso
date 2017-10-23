import sys
import random
from itertools import izip
from PIL import Image
import numpy as np 
import cv2 as cv
from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average

class SourceImg():
    """ Source images """

    def __init__(self, imgFile):
        self.imgFile = Image.open(imgFile)
        self.sizex = self.imgFile.size[0]
        self.sizey =self.imgFile.size[1]
        self.data = self.imgFile.getdata()

class Canvas():
    """ A blank, black canvas """

    def __init__(self, SourceImg):
        self.sizex = SourceImg.sizex
        self.sizey = SourceImg.sizey
        self.imgArray = np.zeros((self.sizex, self.sizey, 3), np.uint8)
        self.imgFile = Image.fromarray(self.imgArray)
        self.data = self.imgFile.getdata()

    def save(self):
        cv.imwrite(sys.argv[2], self.imgArray)

class TestCanvas(Canvas):
    """ An intermediate canvas for data processing """

    def __init__(self, Canvas):
        self.sizex = Canvas.sizex
        self.sizey = Canvas.sizey
        self.imgArray = Canvas.imgArray

    def addShape(self, shape):
        if shape == "line":
            self.line()

    def line(self):
        self.imgArray = cv.line(self.imgArray,(random.randrange(self.sizex),random.randrange(self.sizey)),(random.randrange(self.sizex),random.randrange(self.sizey)),(random.randrange(256),random.randrange(256),random.randrange(256)),1)

    def save(self):
        cv.imwrite(sys.argv[2], self.imgArray)

def compare(a, b):
    pairs = izip(a, b)
    if len(Canvas.imgFile.getbands()) == 1:
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2)

        ncomponents = Canvas.imgFile.size[0] * self.imgFile
