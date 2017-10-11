import sys
import random
from itertools import izip
from PIL import Image
import numpy as np 
import cv2 as cv

class SourceImg():
    """ An attempt to model an image """

    def __init__(self, imgfile):
        """Initialize name and age attributes."""
        self.imgfile = Image.open(imgfile)
        #set all these
        self.sizex = self.imgfile.size[0]
        self.sizey =self.imgfile.size[1]
        self.imgArray = np.asarray(self.imgfile)

class DestImg():
    """ An attempt to model an image """

    def __init__(self, SourceImg):
        """ Initialize xsize and ysize these
            will most likely be made to the
            dimensions of the source file    """
        self.sizex = SourceImg.sizex
        self.sizey = SourceImg.sizey
        self.imgArray = np.zeros((self.sizex, self.sizey, 3), np.uint8)
        self.diff = percentageDiff(self.imgArray, SourceImg.imgArray)


    def addShape(self, shapetype):
        trial = self.imgArray
        if shapetype == "line":
            trial = cv.line(trial,(random.randrange(self.sizex),random.randrange(self.sizey)),(random.randrange(self.sizex),random.randrange(self.sizey)),(random.randrange(256),random.randrange(256),random.randrange(256)),3)
            if (percentageDiff(trial, self.imgArray)) < self.diff:
                self.imgArray = trial
            else:
                self.addShape(shapetype)

    def save(self, name):
        cv.imwrite(name, self.imgArray)


def percentageDiff(a, b):
    #return np.mean( a != b )
    return ((a - b) ** 2).mean(axis=ax)

source = SourceImg("image1.jpg")
print( "source.sizex: ", source.sizex )
print( "source.sizey: ", source.sizey )

print()

test = DestImg(source)
print( "test.sizex: ", test.sizex )
print( "test.sizey: ", test.sizey )

print test.diff
test.addShape("line")
print test.diff
count = 0
#while test.diff > 0.1:
#    test.addShape("line")
#    print(test.diff)
#    count += 1
#    if count % 50 == 0:
#        test.save("test.jpg")



test.save("test.jpg")
