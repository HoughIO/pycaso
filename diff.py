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

class DestImg():
  """ An attempt to model an image """

  def __init__(self, SourceImg):
    """Initialize the destination image, or the canvas"""
    self.sizex = SourceImg.sizex
    self.sizey = SourceImg.sizey
    self.imgArray = np.zeros((self.sizex, self.sizey, 3), np.uint8)
    self.imgArrayTest = self.imgArray
    self.imgFile = Image.fromarray(self.imgArray)
    self.imgFileTest = Image.fromarray(self.imgArrayTest)
    self.imgData = self.imgFile.getdata()
    self.imgDataTest = self.imgFileTest.getdata()
    self.diff = self.percentageDiff(SourceImg)

  def addShape(self, SourceImg, shapetype):
    if shapetype == "line":
      self.addLine(SourceImg)

  def addLine(self, SourceImg):
    #Adds a line to the test array
    self.imgArrayTest = cv.line(self.imgArray,(random.randrange(self.sizex),random.randrange(self.sizey)),(random.randrange(self.sizex),random.randrange(self.sizey)),(random.randrange(256),random.randrange(256),random.randrange(256)),1)
    #Creates an image file in memory from the test array
    self.updateImageData()
    if (self.percentageDiff(SourceImg)) > self.diff:
      self.imgArray = self.imgArrayTest
      self.updateImageData()
      self.diff = self.percentageDiff(SourceImg)
    else:
      self.imgArrayTest = self.imgArray
      self.updateImageData()

  def save(self):
    cv.imwrite(sys.argv[2], self.imgArray)
    if hasattr(self, 'imgFile'):
      self.imgData = self.imgFile.getdata()

  def updateImageData(self):
    self.imgFileTest = Image.fromarray(self.imgArrayTest)
    self.imgDataTest = self.imgFileTest.getdata()

  def percentageDiff(self, SourceImg):
    #return np.mean( a != b )
    pairs = izip(SourceImg.imgData, self.imgDataTest)
    if len(SourceImg.imgFile.getbands()) == 1:
      # for gray-scale jpegs
      dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
      dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))

      ncomponents = SourceImg.imgFile.size[0] * self.imgFileTest.size[1] * 3
      return (dif / 255.0 * 100) / ncomponents

#garbage testing below, ignore

source = SourceImg(sys.argv[1])
print( "source.sizex: ", source.sizex )
print( "source.sizey: ", source.sizey )

test = DestImg(source)
print "test.sizex: ", test.sizex
print "test.sizey: ", test.sizey

count = 0
while test.diff < 90.0:
  test.addShape(source, "line")
  print "Start: ", test.diff," Current: ", test.percentageDiff(source)
  count += 1
  if count % 100 == 0:
    test.save()



test.save()
