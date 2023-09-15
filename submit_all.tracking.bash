#!/bin/sh -l
#
# This script submits the jobs to run the tracking.py script
#
# Usage: submit_all.tracking.bash <year>
#
# For example: bash submit_all.tracking.bash 2005
#

# Check that the year has been provided
if [ $# -ne 1 ]; then
    echo "Usage: submit_all.unique_cells.bash <year>"
    exit 1
fi

# extract the year from the command line
year=$1

# echo the year
echo "Tracking for year: $year"


# set up the extractor script
EXTRACTOR="/data/users/hgilmour/initial_tracks/tobac_initial_tracks/submit.tracking.sh"

# base directory is the directories where the tb and features files are stored
base_dir_tb="/data/users/hgilmour/tb"
base_dir_features="/data/users/hgilmour/initial_tracks/tobac_initial_tracks/feature_detection"


# Set up the output directory
OUTPUT_DIR="/data/users/hgilmour/initial_tracks/tobac_initial_tracks/lotus_output/tracking"
mkdir -p $OUTPUT_DIR

# Find the tb files for the given year
tb_file="tb_${year}.nc"
# construct the tb path
tb_path=${base_dir_tb}/${tb_file}

# Find the features files for the given year
features_file="features_${year}.h5"
# construct the features path
features_path=${base_dir_features}/${features_file}



# Set up the output files
OUTPUT_FILE="$OUTPUT_DIR/all_tracking.$year.out"
ERROR_FILE="$OUTPUT_DIR/all_tracking.$year.err"

# submit the batch job
sbatch --mem=100000 --ntasks=4 --time=40 --output=$OUTPUT_FILE --error=$ERROR_FILE $EXTRACTOR $features_path $tb_path
    
done
