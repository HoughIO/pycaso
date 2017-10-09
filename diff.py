import sys
import random
from itertools import izip
from PIL import Image
import numpy as np
import cv2 as cv

def pxcompare(sourceimg, outputimg):
  i1 = Image.open(sourceimg)
  i2 = Image.open(outputimg)
  assert i1.mode == i2.mode, "Different kinds of images."
  assert i1.size == i2.size, "Different sizes."
  pairs = izip(i1.getdata(), i2.getdata())
  if len(i1.getbands()) == 1:
      # for gray-scale jpegs
      dif = sum(abs(p1-p2) for p1,p2 in pairs)
  else:
      dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
  ncomponents = i1.size[0] * i1.size[1] * 3
  return ((dif / 256.0 * 100) / ncomponents)

def drawcanvas(sourceimg):
  i1 = Image.open(sourceimg)
  output = np.zeros((i1.size[0],i1.size[1],3), np.uint8)
  return output
  #This code was to render to the screen.
  #cv.imshow('output', output)
  #cv.waitKey(0)

def getsourcesize(sourceimg):
  i1 = Image.open(sourceimg)
  return i1.size

def saveimg(outputname, imginput):
  cv.imwrite(outputname, imginput)

def addshape(img, shapetype):
  #So here I want to be able to pass in the current image
  #and pass in a type of shape (rectangle, square, etc.)
  #This should return the updated image
  size = getsourcesize(sys.argv[1])
  if shapetype == "line":
    cv.line(img,(random.randrange(size[0]),random.randrange(size[1])),(random.randrange(size[0]),random.randrange(size[1])),(random.randrange(256),random.randrange(256),random.randrange(256)),5)
    cv.imwrite("test.jpg", img)

likeness = pxcompare(sys.argv[1], sys.argv[2])
print(likeness)
output = drawcanvas(sys.argv[1])
addshape(output, "line")
print(pxcompare(sys.argv[1], sys.argv[2]))

while likeness < 50:
  addshape(output, "line")
  likeness = pxcompare(sys.argv[1], sys.argv[2])
  print likeness
