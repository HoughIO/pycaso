import sys
import time
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
        self.diff = float

class Canvas(SourceImg):
    """ A blank, black canvas """

    def __init__(self, SourceImg):
        self.sizex = SourceImg.sizex
        self.sizey = SourceImg.sizey
        self.imgArray = np.zeros((self.sizex, self.sizey, 3), np.uint8)
        self.imgFile = Image.fromarray(self.imgArray)
        self.data = self.imgFile.getdata()
        self.bands = self.imgFile.getbands()
        self.diff = 99.0


    def addShape(self, shape):
        if shape == "line":
            self.line()
        if shape == "rectangle":
            self.rectangle()

    def line(self):
        self.imgArray = cv.line(self.imgArray,(random.randrange(self.sizex),random.randrange(self.sizey)),(random.randrange(self.sizex),random.randrange(self.sizey)),(random.randrange(256),random.randrange(256),random.randrange(256)),1)

    def rectangle(self):
        self.imgArray = cv.rectangle(self.imgArray,(random.randrange(self.sizex),random.randrange(self.sizey)),(random.randrange(self.sizex),random.randrange(self.sizey)),(random.randrange(256),random.randrange(256),random.randrange(256)),1)

    #added name for testing
    def save(self, name):
        if name:
          cv.imwrite(name, self.imgArray)
        cv.imwrite(sys.argv[2], self.imgArray)

def compare(Image1, Image2):
    Image2.imgFile = Image.fromarray(Image2.imgArray)
    Image2.data = Image2.imgFile.getdata()
    Image2.bands = Image2.imgFile.getbands()
    pairs = izip(Image1.data, Image2.data)
    if len(Image1.bands) == 1:
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
        ncomponents = Image1.imgFile.size[0] * Image2.imgFile.size[1] * 3
        Image2.diff = (dif / 255.0 * 100) / ncomponents
        return (dif / 255.0 * 100) / ncomponents

source = SourceImg(sys.argv[1])
print "source.sizex: ", source.sizex
print "source.sizey: ", source.sizey

canvas = Canvas(source)
print "canvas.sizex: ", canvas.sizex
print "canvas.sizey: ", canvas.sizey

test = Canvas(canvas)
print "test.sizex: ", test.sizex
print "test.sizey: ", test.sizey

compare(source, canvas)
print canvas.diff
print source.diff

yes = 0
no = 0
count = 0

while source.diff > 20:
  test.addShape("line")
  compare(source, test)

  if test.diff < canvas.diff:
    print  canvas.diff, test.diff, "yes: ", yes, "no: ", no
    canvas.imgArray = test.imgArray
    canvas.data = test.data
    canvas.imgFile = Image.fromarray(canvas.imgArray)
    canvas.data = canvas.imgFile.getdata()
    compare(source, canvas)
    yes += 1
    canvas.save(str(count) + ".jpg")
  else:
    print  canvas.diff, test.diff, "yes: ", yes, "no: ", no
    test.imgArray = []
    test.imgArray = canvas.imgArray
    test.imgFile = Image.fromarray(canvas.imgArray)
    compare(source, test)
    no += 1
  count += 1
canvas.save()
