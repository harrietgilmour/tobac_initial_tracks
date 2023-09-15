# Python script for tracking of MCSs using tobac.
# Tracking is output as annual files to remove the issues with tracking over monthly boundaries
#
# <USAGE> python tracking.py <FEATURES_FILE> <TB_FILE>
#
# <EXAMPLE> python tracking.py /data/users/hgilmour/initial_tracks/tobac_initial_tracks/feature_detection/features_merge_1998.h5 /data/users/hgilmour/tb/tb_1998.nc

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
    if len(args) != 3:
        print("Incorrect number of arguements")
        print("Usage: python tracking.py <FEATURES_FILE> <TB_FILE>")
        print("Example: python tracking.py /data/users/hgilmour/initial_tracks/tobac_initial_tracks/feature_detection/features_merge_1998.h5 /data/users/hgilmour/tb/tb_1998.nc")
        sys.exit(1)

# Write a function which loads the files
def open_datasets(features_file, tb_file):
    """ Load specified files"""

    features = iris.load_cube(features_file)
    tb = iris.load_cube(tb_file)

    return features, tb

# Define main function 
def main():
    #First extract the arguments:
    features_file = str(sys.argv[1])
    tb_file = str(sys.argv[2])

    # We want to extract the month and year from the tb_file path
    # An example of the path is:
    # /data/users/hgilmour/initial_tracks/tobac_initial_tracks/features_merge_01_2005.nc
    # Extract the filename first
    filename = os.path.basename(features_file)
    print("Type of filename:", type(filename))
    print("Filename:", filename)

    filename = filename.replace(".", "_")
    segments = filename.split("_")
    print(segments)

    year = segments[3]

    # Print the year
    print("year", year)

    # Open the dataset
    features, tb = open_datasets(features_file, tb_file)    

    # Determine temporal and spatial sampling of the input data:
    dxy,dt=tobac.get_spacings(tb,grid_spacing=4500,time_spacing=3600) #time spacing = 1 hour

    # Linking:
    parameters_linking={}
    parameters_linking['v_max']=60 #(velocity of 60 m s-1 is referenced in https://journals.ametsoc.org/view/journals/mwre/126/6/1520-0493_1998_126_1630_lcvomc_2.0.co_2.xml#i1520-0493-126-6-1630-f01 study)
    parameters_linking['stubs']=7 #minimum number of timesteps for a tracked cell to be reported (equivalent to 6 hours)
    parameters_linking['order']=1
    parameters_linking['extrapolate']=0 
    parameters_linking['memory']=0
    parameters_linking['adaptive_stop']=0.2
    parameters_linking['adaptive_step']=0.95
    parameters_linking['subnetwork_size']=15
    parameters_linking['method_linking']= 'predict'

    tracking_filename = f"tracks_{year}.h5"
    print("tracking filename", tracking_filename)

    tracking_savepath = "tracking" + "/" + tracking_filename

    # Perform linking and save results to file:
    Track=tobac.linking_trackpy(features,tb,dt=dt,dxy=dxy,**parameters_linking)
    Track["longitude"]=Track["longitude"]-360
    Track.to_hdf(tracking_savepath, 'table')

#Run the main function
if __name__ == "__main__":
    main()