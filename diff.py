import sys
from itertools import izip
from PIL import Image

def pxcompare(image1, image2):
  i1 = Image.open(image1)
  i2 = Image.open(image2)
  assert i1.mode == i2.mode, "Different kinds of images."
  assert i1.size == i2.size, "Different sizes."
  pairs = izip(i1.getdata(), i2.getdata())
  if len(i1.getbands()) == 1:
      # for gray-scale jpegs
      dif = sum(abs(p1-p2) for p1,p2 in pairs)
  else:
      dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
  ncomponents = i1.size[0] * i1.size[1] * 3
  print "Difference (percentage):", (dif / 255.0 * 100) / ncomponents


pxcompare(sys.argv[1], sys.argv[2])
