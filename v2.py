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
        self.bands = self.imgFile.getbands()

class Canvas():
    """ A blank, black canvas """

    def __init__(self, SourceImg):
        self.sizex = SourceImg.sizex
        self.sizey = SourceImg.sizey
        self.imgArray = np.zeros((self.sizex, self.sizey, 3), np.uint8)
        self.imgFile = Image.fromarray(self.imgArray)
        self.data = self.imgFile.getdata()
        self.bands = self.imgFile.getbands()

    def save(self):
        cv.imwrite(sys.argv[2], self.imgArray)

class TestCanvas(Canvas):
    """ An intermediate canvas for data processing """

    def __init__(self, Canvas):
        self.sizex = Canvas.sizex
        self.sizey = Canvas.sizey
        self.imgArray = Canvas.imgArray
        self.imgFile = Canvas.imgFile
        self.data = Canvas.data
        self.bands = Canvas.bands

    def addShape(self, shape):
        if shape == "line":
            self.line()

    def line(self):
        self.imgArray = cv.line(self.imgArray,(random.randrange(self.sizex),random.randrange(self.sizey)),(random.randrange(self.sizex),random.randrange(self.sizey)),(random.randrange(256),random.randrange(256),random.randrange(256)),1)

    def save(self):
        cv.imwrite(sys.argv[2], self.imgArray)


def compare(Image1, Image2):
    #called like compare(canvas.data, source.data, canvas.bands)
    pairs = izip(Image1.data, Image2.data)
    if len(Image1.bands) == 1:
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
        ncomponents = Image1.imgFile.size[0] * Image2.imgFile.size[1] * 3
        return (dif / 255.0 * 100) / ncomponents


source = SourceImg(sys.argv[1])
print "source.sizex: ", source.sizex
print "source.sizey: ", source.sizey

canvas = Canvas(source)
print "canvas.sizex: ", canvas.sizex
print "canvas.sizey: ", canvas.sizey

test = TestCanvas(canvas)
print "test.sizex: ", test.sizex
print "test.sizey: ", test.sizey

print compare(source, canvas)
print compare(canvas, test)

test.addShape("line")
test.save()
print compare(canvas, test)

