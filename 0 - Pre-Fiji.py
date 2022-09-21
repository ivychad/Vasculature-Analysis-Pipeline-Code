
# import libraries

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
from skimage import io
import time
import tifffile as tif

# Magic numbers

# CHANGE WITH EVERY NEW DATASET
STACKSIZE = 1001
DATA = "V2 Binary.tif"
COORFILE = np.asarray(pd.read_excel(r"CoorTemplate.xlsx", sheet_name= "V2"))


# Fixed variables
# set the filling of the polygon, can be anything but 0, does not matter, because that is the part we do not need
EMPTY = 2
BLACK = 0

# number of x,y coordinate tuples in the layer polygon (when using new method, always the same)
COORCOUNT = 24


def layercropping(coorfile, layernumber, savefile):
    
    # open datafile an convert to stack, clear memory of large image file
    stack = io.imread(DATA)
    stackarr = np.asarray(stack)
    del stack
    
    #  local variables
    itrpltd_dist = []
    layertop = []
    layerbot = []
    layer_stack = []

    # make polygon for top of stack (layertop) and bottom of stack (layerbot) by appending the upper and lower layer bound lines
    # add top line
    for n in range(12):
        layertop.append(tuple((coorfile[layernumber-1][n],coorfile[layernumber-1][12+n])))
        layerbot.append(tuple((coorfile[layernumber+3][n],coorfile[layernumber+3][12+n])))

    # add bottom line
    for n in range(12, 0,-1):
        layertop.append(tuple((coorfile[layernumber][n-1],coorfile[layernumber][n+11])))
        layerbot.append(tuple((coorfile[layernumber+4][n-1],coorfile[layernumber+4][n+11])))

    # calculate the difference between top and bottom polygon y-coordinates, the difference
    # by stack size -1 = number of images that need to be interpolated
    for n in range(COORCOUNT):
        diff = layertop[n][1]-layerbot[n][1]
        dist = diff/(STACKSIZE-1)
        itrpltd_dist.append(dist)

    # fill a stack of size stack_size (size of data stack) with coordinates of top layer -> will be changed for each image in next step
    arr1 = np.array(layertop)
    stack_coordinates = [arr1]*STACKSIZE
    stack_coord = np.asarray(stack_coordinates)

    # get an array for the interpolated coordinates for all images -> image coordinate - interpolated distance
    for n in range(STACKSIZE):        
        for i in range(COORCOUNT):         
            stack_coord[n][i][1] = stack_coord[n][i][1] - itrpltd_dist[i]*n

    # crop stack image by image to polygon and then create new stack with cropped images       
    for i in range(STACKSIZE):
        
        # select current image
        currentimage = stackarr[i]
        polygon = []

        # make calculated coordinates to tuples (only way they can be fed into the polygon drawing function)
        for n in range (COORCOUNT):
            coordpair = tuple(stack_coord[i][n])
            polygon.append(coordpair)
        
        # create empty image with same image as the data image
        maskIm = Image.new('L', (currentimage.shape[1], currentimage.shape[0]), BLACK)
        
        # draw polygon mask into empty image (fill polygon with 2s)
        ImageDraw.Draw(maskIm).polygon(polygon, outline=EMPTY, fill=EMPTY)
        arraymask = np.array(maskIm)
        
        # set selected image to 0 (black) where there is no filled polygon -> leaves the polygon data
        currentimage[arraymask!=EMPTY]=BLACK
        
        # append cropped image to new cropped image stack
        layer_stack.append(currentimage)
    
    # convert layer polygons to array
    arr_layertop = np.array(layertop)
    arr_layerbot = np.array(layerbot)
    
    # get for both top and bottom polygon the min and max y value
    MIN_top = min(arr_layertop[:,1])
    MAX_top = max(arr_layertop[:,1])
    MIN_bottom = min(arr_layerbot[:,1])
    MAX_bottom = max(arr_layerbot[:,1])

    # get overall min and max y value -> for whole stack
    MIN = min(MIN_top,MIN_bottom)
    MAX = max(MAX_top,MAX_bottom)

    # crop away top and bottom of image that does not contain data (data: between min & max)
    layer_stack = np.asarray(layer_stack)
    layer_stack_crop = layer_stack[:,MIN:MAX]

    # save layer stack as tiff file
    tif.imwrite(savefile, layer_stack_crop, bigtiff=True)

# run function for layers, input name the layer stack tiff should be saved as
#layer1 = layercropping(COORFILE, 1, "layer1.tif")
#layer2 = layercropping(COORFILE, 2, "layer2.tif")
#layer3 = layercropping(COORFILE, 3, "layer3.tif")


def straightening_coor(coorfile, layernumber, filename):
    upper_layertop = []
    upper_layerbot = []
    lower_layertop = []
    lower_layerbot = []

    coorfile = coorfile[:,1:]

    for n in range(12):
        upper_layertop.append([coorfile[layernumber-1][n],coorfile[layernumber-1][12+n]])
        upper_layerbot.append([coorfile[layernumber+3][n],coorfile[layernumber+3][12+n]])
        lower_layertop.append([coorfile[layernumber][n],coorfile[layernumber][12+n]])
        lower_layerbot.append([coorfile[layernumber+4][n],coorfile[layernumber+4][12+n]])

    straight_top = []
    straight_bot = []

    for i in range(12):
        dis_y_top = (lower_layertop[i][1]-upper_layertop[i][1])/2
        dis_y_bot = (lower_layerbot[i][1]-upper_layerbot[i][1])/2
        y_top = dis_y_top + upper_layertop[i][1]
        y_bot = dis_y_bot + upper_layerbot[i][1]
        upper_layertop[i][1] = y_top
        upper_layerbot[i][1] = y_bot
        straight_top = upper_layertop
        straight_bot = upper_layerbot


    itrpltd_dist = []

    # calculate the difference between top and bottom polygon y-coordinates, the difference
    # by stack size -1 = number of images that need to be interpolated

    for n in range(12):
         diff = straight_top[n][1]-straight_bot[n][1]
         dist = diff/(STACKSIZE-1)
         itrpltd_dist.append(dist)

    # fill a stack of size stack_size (size of data stack) with coordinates of top layer -> will be changed for each image in next step
    arr1 = np.array(straight_top)
    stack_coordinates = [arr1]*STACKSIZE
    stack_coord = np.asarray(stack_coordinates)

    # get an array for the interpolated coordinates for all images -> image coordinate - interpolated distance

    for n in range(STACKSIZE):        
        for i in range(12):         
            stack_coord[n][i][1] = stack_coord[n][i][1] - itrpltd_dist[i]*n
    
    straight_coord = []
    straight_coordinates = []

    for n in range(STACKSIZE):
        straight_coord = []
        for i in range(12):
                straight_coord.append(stack_coord[n][i][0])
                straight_coord.append(stack_coord[n][i][1])      
        straight_coordinates.append(straight_coord)

    straight_coordinates = np.asarray(straight_coordinates)
    straight_coord_round = np.around(straight_coordinates,2) 

    # save to excel file with filename  
    np.savetxt(filename, straight_coord_round, delimiter=',') 


#straight_layer1 = straightening_coor(COORFILE, 1, "V2 Layer1 StraightCoor.csv")
#straight_layer2 = straightening_coor(COORFILE, 2, "V2 Layer2 StraightCoor.csv")
#straight_layer3 = straightening_coor(COORFILE, 3, "V2 Layer3 StraightCoor.csv")