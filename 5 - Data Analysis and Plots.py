# -*- coding: utf-8 -*-
"""
Script for Data Analysis of Excel file with Orientation values for all layers and images

@author: hanna hoogen

- add Yuliyas statistics script?


"""


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# array with x axis data of orientation in degrees between -89.5 and 89.5 in steps of 1
orientation = np.empty(180)
filler = np.arange(-89.5,90.5,1)
index = np.arange(orientation.size)
np.put(orientation,index,filler)


# arrays with the data for each of the four layers
array_1 = pd.read_excel(r"C:\Users\hanna\Desktop\V1 Straight Analysis.xlsx", sheet_name="1")
array_2 = pd.read_excel(r"C:\Users\hanna\Desktop\V1 Straight Analysis.xlsx", sheet_name="2")
array_3 = pd.read_excel(r"C:\Users\hanna\Desktop\V1 Straight Analysis.xlsx", sheet_name="3")
#array_4 = pd.read_excel(r"C:\Users\hanna\Desktop\V1 Straight.xlsx", sheet_name="4")
array_1 = np.asarray(array_1)
array_2 = np.asarray(array_2)
array_3 = np.asarray(array_3)
#array_4 = np.asarray(array_4)


array_1 = np.delete(array_1,[0],axis=0)
array_1 = np.delete(array_1,[0,1,202,203,204,405,406,407,608,609,610,811,812,813],axis=1)
array_2 = np.delete(array_2,[0],axis=0)
array_2 = np.delete(array_2,[0,1,202,203,204,405,406,407,608,609,610,811,812,813],axis=1)
array_3 = np.delete(array_3,[0],axis=0)
array_3 = np.delete(array_3,[0,1,202,203,204,405,406,407,608,609,610,811,812,813],axis=1)


# size of the analyzed stack
Stack_size = 1001

# name of the dataset for the figure
data_set_name = ""


def analysis(data_array, stack_size):
    # function to get mean and std of the data
    
    pixel_sum = []
    slice_percent = np.empty(shape=[180,stack_size])
    mean = []
    std = []
    data = []
    
    for i in range(stack_size):        
        # get sum of pixel count for each slice over all orientations
        pixel_sum.append(sum(data_array[:,i]))
    
    for a in range(stack_size):
        for n in range(180):
            # divide each slice orientation value by total pixel count 
            # -> percentage of total pixels for each slice
            slice_percent[n,a] = data_array[n,a]/pixel_sum[a]
            
    for h in range(180):
        # get mean and standard deviation of percentage of total pixels
        mean.append(np.mean(slice_percent[:][h]))
        std.append(np.std(slice_percent[:][h]))
        
    data.append(mean)
    data.append(std)
    return data

# create variable that contains the return array with mean and std for layer
layer_1 = analysis(array_1, Stack_size)
layer_2 = analysis(array_2, Stack_size)
layer_3 = analysis(array_3, Stack_size)
#layer_4 = analysis(array_4, Stack_size)

layer_1 = np.array(layer_1)
layer_2 = np.array(layer_2)
layer_3 = np.array(layer_3)
#layer_4 = np.array(layer_4)

# change from decimals to percentage
layer_1 = layer_1*100
layer_2 = layer_2*100
layer_3 = layer_3*100
#layer_4 = layer_4*100


#print(orientation)

# plot

plt.figure(figsize=(16, 9))
plt.errorbar(orientation, layer_1[0], yerr=layer_1[1], color='lightcoral')
plt.errorbar(orientation, layer_2[0], yerr=layer_2[1], color="khaki")
plt.errorbar(orientation, layer_3[0], yerr=layer_3[1], color=(0.33, 0.67, 1))
#plt.errorbar(orientation, layer_4[0], yerr=layer_4[1], color=(0.33, 0.67, 1))
plt.errorbar(orientation, layer_1[0], label="Layer 1", color="crimson")
plt.errorbar(orientation, layer_2[0], label="Layer 2", color="goldenrod")
plt.errorbar(orientation, layer_3[0], label="Layer 3", color="steelblue")
#plt.errorbar(orientation, layer_4[0], label="Layer 4", color="steelblue")
plt.xticks(range(-90, 91, 45), fontsize=25, fontweight="bold")
plt.yticks(np.arange(0.4,1.4,0.2), fontsize=25, fontweight="bold")
#plt.legend(loc="best", fontsize=22, frameon=False)
plt.ylim((0.2,1.25))


#plt.title(data_set_name, fontsize=25, fontweight="bold")
#leg = plt.legend(loc=(0.65,0.7), fontsize=22, frameon=False)
#leg = plt.legend(loc=(0.77,0.7), fontsize=22, frameon=False)
#leg.get_lines()[0].set_linewidth(4)
#leg.get_lines()[1].set_linewidth(4)
#leg.get_lines()[2].set_linewidth(4)
#leg.get_lines()[3].set_linewidth(4)

