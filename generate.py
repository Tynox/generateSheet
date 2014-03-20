#!usr/bin/env python

import sys
import os
import getopt
import codecs
import math
import xml.dom.minidom
from PIL import Image

image_path = sys.argv[1]
image = Image.open(image_path)
width, height = image.size

# calculate leftWidth, centerWidth, rightWidth
if width % 3 == 0:
    lw = cw = rw = width / 3
else:
    tempW = int(math.floor(width / 4))
    lw = rw = tempW
    cw = width - lw - rw
    
# calculate topHeight, centerHeight, bottomHeight
if height % 3 == 0:
    th = ch = bh = height / 3
else:
    tempH = int(math.floor(height / 4))
    th = bh = tempH
    ch = height - th - bh
    
x1 = 0
x2 = lw
x3 = lw + cw
y1 = 0
y2 = th
y3 = th + ch
    
print "width: {0} {1} {2}".format(lw, cw, rw)
print "height: {0} {1} {2}".format(th, ch, bh)


# generate .sheet
impl = xml.dom.minidom.getDOMImplementation()
dom = impl.createDocument(None, "sheet", None)
root = dom.documentElement
root.setAttribute("texture", image_path[image_path.rfind("/")+1:])

for row, s in zip([["lt", "t", "rt"], ["l", "m", "r"], ["lb", "b", "rb"]], [zip([lw, cw, rw],[th, th, th]), zip([lw, cw, rw],[ch, ch, ch]), zip([lw, cw, rw], [bh, bh, bh])]):
    for name, size in zip(row, s):
        w, h = size
        if "t" in name:
            y = y1
        elif "b" in name:
            y = y3
        else:
            y = y2
        if "l" in name:
            x = x1
        elif "r" in name:
            x = x3
        else:
            x = x2
            
        ele = dom.createElement("sprite")
        ele.setAttribute("name", str(name))
        ele.setAttribute("x", str(x))
        ele.setAttribute("y", str(y))
        ele.setAttribute("width", str(w))
        ele.setAttribute("height", str(h))
        root.appendChild(ele)

sheet_file_name = "{0}.sheet".format(image_path[: image_path.rfind(".")])        
print sheet_file_name
out = codecs.open(sheet_file_name, "w", "utf-8")
dom.writexml(out, newl="\n")
out.close()