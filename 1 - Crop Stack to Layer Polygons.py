# -*- coding: utf-8 -*-
"""
Created on Sat May 28 11:21:23 2022

@author: hanna hoogen

3D Polygon Layer cropping & Orientation analysis with Fiji

ToDo
- as many constants and variables as possible -> everything that has to be tuned should be at the beginning
- import coordinates from file
- loop so all 4 layers are run automatically without having to change the layer numbers in the variables
- rename teststack
- more efficent coordinate selection -> set x coordinates (every 100 pixel or so) draw top line for each layer + bottom of last layer
script that automatically makes a polygon of the lines so they fit exactly to each other
- add all layer automated second script to this script

- make script flexible to other tissues etc. so that there is one blog that only does the cropping into polygons and can take any coordinates





"""


# import libraries

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
from skimage import io
import time
from skimage.external import tifffile as tif

start_time = time.time()

# coordinates for matching layer polygons at top and bottom of stack

# 20
layer1_top = [(0, 6), (183, 45), (405, 72), (642, 105), (876, 102), (1098, 81), (1335, 0), (2048,
              0), (2048, 18), (1929, 75), (1800, 126), (1644, 177), (1473, 234), (1287, 285), 
              (1086, 330), (870, 345), (642, 333), (399, 297), (177, 252), (0, 201)]

layer1_bottom = [(0, 85), (183, 180), (405, 240), (642, 246), (876, 230), (1098, 220), (1335, 150), (2048, 0), (2048, 
                 120), (1929, 177), (1800, 252), (1644, 321), (1473, 395), (1287, 430), (1086, 460), (870, 490), (642, 490),
                 (399, 490), (177, 440), (0, 340)]

# 23
layer2_top = [(0, 201), (177, 252), (399, 297), (642, 333), (870, 345), (1086, 330), (1287, 
              285), (1473, 234), (1644, 177), (1800, 126), (1929, 75), (2048, 18), (2048, 360),
              (1776, 456), (1548, 540), (1335, 612), (1176, 657), (1011, 681), (831, 696), (615, 
              708), (399, 693), (213, 660), (0, 594)]

layer2_bottom = [(0, 340), (177, 440), (399, 490), (642, 490), (870, 490), (1086, 460), (1287, 
              430), (1473, 395), (1644, 321), (1800, 252), (1929, 177), (2048, 120), (2048, 560),
              (1776, 680), (1548, 790), (1335, 895), (1176, 960), (1011, 1010), (831, 1040), (615, 
              1015), (399, 960), (213, 900), (0, 800)]

# 21
layer3_top = [(0, 594), (213, 660), (399, 693), (615, 708), (831, 696), (1011, 681), (1176, 657),
              (1335, 612), (1548, 540), (1776, 456), (2048, 360), (2048, 747), (1746, 843), (1515,
              897), (1311, 939), (1101, 987), (816, 993), (582, 987), (387, 969), (171, 948), (0, 912)]

layer3_bottom = [(0, 800), (213, 900), (399, 960), (615, 1015), (831, 1040), (1011, 1010), (1176, 960),
              (1335, 895), (1548, 790), (1776, 680), (2048, 560), (2048, 970), (1746, 1110), (1515,
              1210), (1311, 1330), (1101, 1400), (816, 1440), (582, 1440), (387, 1410), (171, 1365), (0, 1270)]

# 20
layer4_top = [(0, 912), (171, 948), (387, 969), (582, 987), (816, 993), (1101, 987), (1311, 939), 
              (1515, 897), (1746, 843), (2048, 747), (2048, 1086), (1815, 1176), (1623, 1233), 
              (1371, 1281), (1161, 1317), (954, 1323), (687, 1332), (423, 1320), (204, 1305), (0, 1272)]

layer4_bottom = [(0, 1270), (171, 1365), (387, 1410), (582, 1440), (816, 1440), (1101, 1400), (1311, 1330), 
              (1515, 1210), (1746, 1110), (2048, 970), (2048, 1300), (1815, 1400), (1623, 1480), 
              (1371, 1545), (1161, 1580), (954, 1605), (687, 1635), (423, 1638), (204, 1593), (0, 1521)]


#%%

# magic numbers

# name of the image stack
FILENAME = "V2 Binary New.tif"
# size of the original image stack
STACKSIZE = 1001
# number of x,y coordinate tuples in the layer polygon (usually between 14 and 22)
COORCOUNT = 20
# name of the file the layer_stack will be saved as
SAVEFILE = 'layer4.tif'
# set the filling of the polygon, can be anything but 0, does not matter, because that is the part we do not need
EMPTY = 2
BLACK = 0



# select which layer should be run (change the number)
layer_top = layer4_top
layer_bottom = layer4_bottom


# variables

# differences between top and bottom polygon for each y coordinate
itrpltd_dist = []
# output image array
layer_stack = []

# image stack that should be cropped
teststack = io.imread(FILENAME)
testarray = np.asarray(teststack)
del teststack

#%%

# calculate the difference between top and bottom polygon y-coordinates, the difference
# by stack size -1 = number of images that need to be interpolated

for n in range(COORCOUNT):
    diff = layer_top[n][1]-layer_bottom[n][1]
    dist = diff/(STACKSIZE-1)
    itrpltd_dist.append(dist)

# fill a stack of size stack_size (size of data stack) with coordinates of top layer -> will be changed for each image in next step
arr1 = np.array(layer_top)
stack_coordinates = [arr1]*STACKSIZE
stack_coord = np.asarray(stack_coordinates)

# get an array for the interpolated coordinates for all images -> image coordinate - interpolated distance

for n in range(STACKSIZE):        
    for i in range(COORCOUNT):         
        stack_coord[n][i][1] = stack_coord[n][i][1] - itrpltd_dist[i]*n



#%%

# crop stack image by image to polygon and then create new stack with cropped images
        
for i in range(STACKSIZE):
    
    # select current image
    testimage = testarray[i]
    polygon = []

    # make calculated coordinates to tuples (only way they can be fed into the polygon drawing function)
    for n in range (COORCOUNT):
        coordpair = tuple(stack_coord[i][n])
        polygon.append(coordpair)
    
    # create empty image with same image as the data image
    maskIm = Image.new('L', (testimage.shape[1], testimage.shape[0]), BLACK)
    
    # draw polygon mask into empty image (fill polygon with 2s)
    ImageDraw.Draw(maskIm).polygon(polygon, outline=EMPTY, fill=EMPTY)
    arraymask = np.array(maskIm)
    
    # set selected image to 0 (black) where there is no filled polygon -> leaves the polygon data
    testimage[arraymask!=EMPTY]=BLACK
    
    # append cropped image to new cropped image stack
    layer_stack.append(testimage)



#%%
    
# crop layer stack

arrlayer_top = np.array(layer_top)
arrlayer_bottom = np.array(layer_bottom)


MIN_top = min(arrlayer_top[:,1])
MAX_top = max(arrlayer_top[:,1])
MIN_bottom = min(arrlayer_bottom[:,1])
MAX_bottom = max(arrlayer_bottom[:,1])

MIN = min(MIN_top,MIN_bottom)
MAX = max(MAX_top,MAX_bottom)

layer_stack = np.asarray(layer_stack)

layer_stack = layer_stack[:,MIN:MAX]



# %%

# save as tiff
tif.imsave(SAVEFILE, layer_stack, bigtiff=True)


print("--- %s seconds ---" % (time.time() - start_time))

plt.imshow(layer_stack[0])








