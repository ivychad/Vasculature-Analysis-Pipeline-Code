# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 13:12:57 2022

@author: hanna

- import coordinates from file -> same file as for script 1





"""


# import libraries

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
from skimage import io
import time


start_time = time.time()


straight1_top = [(0, 185), (175, 250), (350, 290), (525, 320), (700, 350), (875, 355), (1050, 340), 
              (1225, 315), (1400, 265), (1575, 200), (1750, 130), (1925, 60), (2048, 0)]

straight1_bottom = [(0, 225), (175, 310), (350, 365), (525, 390), (700, 390), (875, 380), (1050, 355), 
              (1225, 320), (1400, 265), (1575, 215), (1750, 155), (1925, 100), (2048, 60)]

straight2_top = [(0, 390), (175, 425), (350, 455), (525, 485), (700, 500), (875, 500), (1050, 480), 
              (1225, 435), (1400, 380), (1575, 320), (1750, 255), (1925, 185), (2048, 135)]

straight2_bottom = [(0, 590), (175, 650), (350, 700), (525, 735), (700, 750), (875, 740), (1050, 700), 
              (1225, 650), (1400, 580), (1575, 510), (1750, 445), (1925, 375), (2048, 310)]

straight3_top = [(0, 395), (175, 460), (350, 495), (525, 515), (700, 520), (875, 510), (1050, 490), 
              (1225, 450), (1400, 410), (1575, 365), (1750, 315), (1925, 255), (2048, 200)]

straight3_bottom = [(0, 685), (175, 760), (350, 830), (525, 870), (700, 895), (875, 900), (1050, 860), 
              (1225, 780), (1400, 700), (1575, 615), (1750, 525), (1925, 445), (2048, 390)]

straight4_top = [(0, 355), (175, 375), (350, 390), (525, 410), (700, 420), (875, 430), (1050, 430), 
              (1225, 410), (1400, 370), (1575, 320), (1750, 270), (1925, 215), (2048, 165)]

straight4_bottom = [(0, 650), (175, 720), (350, 765), (525, 800), (700, 815), (875, 805), (1050, 765), 
              (1225, 715), (1400, 645), (1575, 580), (1750, 510), (1925, 430), (2048, 380)]



#%%

LINECOORCOUNT = 13


# select which layer should be run
line_top = straight4_top
line_bottom = straight4_bottom


# variables

# differences between top and bottom polygon for each y coordinate
itrpltd_dist = []
# output image array
layer_stack = []

straight_line_coor = []

STACKSIZE = 1001
FILENAME = "V1 Layer4 StraightCoor.csv"

#%%

# calculate the difference between top and bottom polygon y-coordinates, the difference
# by stack size -1 = number of images that need to be interpolated

for n in range(LINECOORCOUNT):
    diff = line_top[n][1]-line_bottom[n][1]
    dist = diff/(STACKSIZE-1)
    itrpltd_dist.append(dist)

# fill a stack of size stack_size (size of data stack) with coordinates of top layer -> will be changed for each image in next step
arr1 = np.array(line_top)
stack_coordinates = [arr1]*STACKSIZE
stack_coord = np.asarray(stack_coordinates)

# get an array for the interpolated coordinates for all images -> image coordinate - interpolated distance

for n in range(STACKSIZE):        
    for i in range(LINECOORCOUNT):         
        stack_coord[n][i][1] = stack_coord[n][i][1] - itrpltd_dist[i]*n
 
straight_coord = []
straight_coordinates = []

for n in range(STACKSIZE):
    straight_coord = []
    for i in range(LINECOORCOUNT):
            straight_coord.append(stack_coord[n][i][0])
            straight_coord.append(stack_coord[n][i][1])      
    straight_coordinates.append(straight_coord)

straight_coordinates = np.asarray(straight_coordinates) 

# save to excel file with filename
   
np.savetxt(FILENAME, straight_coordinates, delimiter=',')        

