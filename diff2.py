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
    """ An attempt to model an image """

    def __init__(self, imgFile):
        """Initialize name and age attributes."""
        self.imgFile = Image.open(imgFile)
        self.imgData = self.imgFile.getdata()
        self.sizex = self.imgFile.size[0]
        self.sizey =self.imgFile.size[1]
        self.imgArray = np.asarray(self.imgFile)
        self.grayArray = self.calcGrayscale()

    def calcGrayscale(self):
      if len(self.imgArray.shape) == 3:
        return average(self.imgArray, -1)
      else:
        return imgArray

class DestImg():
    """ An attempt to model an image """

    def __init__(self, SourceImg):
        """ Initialize xsize and ysize these
            will most likely be made to the
            dimensions of the source file    """
        self.sizex = SourceImg.sizex
        self.sizey = SourceImg.sizey
        self.imgArray = np.zeros((self.sizex, self.sizey, 3), np.uint8)
        self.grayArray = self.calcGrayscale()
        self.save()
        self.imgFile = Image.open(sys.argv[2])
        self.imgData = self.imgFile.getdata()
        self.diff = self.percentageDiff(SourceImg)

    def addShape(self, SourceImg, shapetype):
        trial = self.imgArray
        if shapetype == "line":
            trial = cv.line(trial,(random.randrange(self.sizex),random.randrange(self.sizey)),(random.randrange(self.sizex),random.randrange(self.sizey)),(random.randrange(256),random.randrange(256),random.randrange(256)),3)
            self.save
            print self.percentageDiff(SourceImg)
            print self.diff
            print
            if (self.percentageDiff(SourceImg)) < self.diff:
                self1.imgArray = trial
            else:
                self.addShape(SourceImg, shapetype)


    def calcGrayscale(self):
      if len(self.imgArray.shape) == 3:
        return average(self.imgArray, -1)
      else:
        return imgArray

    def save(self):
        cv.imwrite(sys.argv[2], self.imgArray)
        if hasattr(self, 'imgFile'):
          self.imgData = self.imgFile.getdata()


    def percentageDiff(self, SourceImg):
        #return np.mean( a != b )
        pairs = izip(SourceImg.imgData, self.imgData)
        if len(SourceImg.imgFile.getbands()) == 1:
          # for gray-scale jpegs
          dif = sum(abs(p1-p2) for p1,p2 in pairs)
        else:
          dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))

          ncomponents = SourceImg.imgFile.size[0] * self.imgFile.size[1] * 3
          return (dif / 255.0 * 100) / ncomponents

#garbage testing below, ignore

source = SourceImg(sys.argv[1])
print( "source.sizex: ", source.sizex )
print( "source.sizey: ", source.sizey )

test = DestImg(source)
print( "test.sizex: ", test.sizex )
print( "test.sizey: ", test.sizey )

print "TEST:"
print test.diff

print test.diff
test.addShape(source, "line")
count = 0
while test.diff > 90:
    test.addShape("line")
    print(test.diff)
    count += 1
    if count % 50 == 0:
        test.save()



test.save
