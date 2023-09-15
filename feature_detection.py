# Python script for feature detection and segmentation of MCSs based on single brightness temp value of 240K using toac
#
# <USAGE> python feature_detection.py <TB_FILE>
#
# <EXAMPLE> python feature_detection.py /data/uers/hgilmour/tb/2005/tb_merge_01_2005.nc
#

# Import local packages
import os
import sys
import glob

# Import third party packages
import iris
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import iris.plot as iplt
import datetime
import shutil
from six.moves import urllib
from pathlib import Path
import trackpy
from iris.time import PartialDateTime
import tobac

# Import and set up warnings
import warnings
warnings.filterwarnings('ignore')

# Define the usr directory for the dictionaries
sys.path.append("/data/users/hgilmour/initial_tracks")

# Import functions and dictionaries
import dictionaries as dic

# Function that will check the number of arguements passed
def check_no_args(args):
    """ Check the number of arguements passed"""
    if len(args) != 2:
        print("Incorrect number of arguements")
        print("Usage: python feature_detection.py <TB_FILE>")
        print("Example: python feature_detection.py /data/uers/hgilmour/tb/2005/tb_merge_01_2005.nc")
        sys.exit(1)


# Write a function which loads the file
def open_dataset(tb_file):
    """ Load specified files"""

    tb = iris.load_cube(tb_file)

    return tb



# Define main function 
def main():
    #First extract the arguments:
    tb_file = str(sys.argv[1])

    # We want to extract the month and year from the tb_file path
    # An example of the path is:
    # /data/users/hgilmour/tb/2005/tb_merge_01_2005.nc
    # Extract the filename first
    filename = os.path.basename(tb_file)
    print("Type of filename:", type(filename))
    print("Filename:", filename)
    filename_without_extension = os.path.splitext(filename)
    #print("Type of filename_without_extension:", type(filename_without_extension))
    #print(filename_without_extension)
    filename = filename.replace(".", "_")
    segments = filename.split("_")
    print(segments)
    #segments = segments.split("_")
    #print(segments)
    month = segments[2]
    year = segments[3]

    # Print the month and the year
    print("month", month)
    print("year", year)

    # check the number of arguements:
    check_no_args(sys.argv)


    # Open the dataset
    tb = open_dataset(tb_file)

    # Determine temporal and spatial sampling of the input data:
    dxy,dt=tobac.get_spacings(tb,grid_spacing=4500,time_spacing=3600) #time spacing = 1 hour

    # Feature detection:
    parameters_features={}
    parameters_features['position_threshold']='weighted_diff'
    parameters_features['sigma_threshold']=0.5
    parameters_features['target']='minimum'
    parameters_features['threshold']=240 #olr threshold equivalent to Tb=225K based on stefan boltzmann equation (145 for 225K, 91 for 200K, 74 for 190K)
    parameters_features['n_min_threshold']=1975 # number of grid points for 40,000km^2 area (7792m = 1 grid space. 4500m x 4500m = 20250000m^2. 40,000km^2 = 4x10^10m^2. 4x10^10 / 20250000 = 1975 (1975 grid cells per 40,000km^2 area)

    features_filename = f"features_{year}_{month}.h5"
    print("features filename", features_filename)

    features_savepath = "feature_detection" + "/" + features_filename

    # Feature detection and save results to file:
    print('starting feature detection')
    Features=tobac.feature_detection_multithreshold(tb,dxy,**parameters_features)
    Features.to_hdf(features_savepath,'table')
    print('feature detection performed and saved')

    # Segmentation
    parameters_segmentation={}
    parameters_segmentation['target']='minimum'
    parameters_segmentation['method']='watershed'
    parameters_segmentation['threshold']=240

    segmentation_filename = f"segmentation_{year}_{month}.nc"
    print("segmentation filename", segmentation_filename)

    segmentation_savepath = "segmentation" + "/" + segmentation_filename

    features_tb_filename = f"features_tb_{year}_{month}.h5"
    print("features_tb filename", features_tb_filename)

    features_tb_savepath = "features_tb" + "/" + segmentation_filename

    # Perform segmentation and save results to files:
    Mask_tb,Features_tb=tobac.segmentation_2D(Features,tb,dxy,**parameters_segmentation)
    print('segmentation tb performed, start saving results to files')
    iris.save([Mask_tb], segmentation_savepath, zlib=True, complevel=4)
    Features_tb.to_hdf(features_tb_savepath, 'table')
    print('segmentation tb performed and saved')

#Run the main function
if __name__ == "__main__":
    main()




