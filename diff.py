import sys
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
  print((dif / 256.0 * 100) / ncomponents)

def drawcanvas(sourceimg):
  i1 = Image.open(sourceimg)
  print(i1.size)
  output = np.zeros((i1.size[0],i1.size[1],3), np.uint8)
  cv.imshow('output', output)
  cv.imwrite("test.jpg", output)
  cv.waitKey(0)

def saveimg(outputname):
  output.save(outputname)

pxcompare(sys.argv[1], sys.argv[2])
drawcanvas(sys.argv[1])

