#!/bin/sh -l
#
# This script submits the jobs to run the feature_detection.py script
#
# Usage: submit_all.feature_detection.bash <year>
#
# For example: bash submit_all.feature_detection.bash 2005
#

# Check that the year has been provided
if [ $# -ne 1 ]; then
    echo "Usage: submit_all.unique_cells.bash <year>"
    exit 1
fi

# extract the year from the command line
year=$1

# echo the year
echo "Finding unique cells for month in year: $year"

# Set the months
months=(01 02 03 04 05 06 07 08 09 10 11 12)

# set up the extractor script
EXTRACTOR="/data/users/hgilmour/initial_tracks/tobac_initial_tracks/submit.feature_detection.sh"

# base directory is the directory where the tb files are stored
# in format tb_merge_mm_yyyy.nc

base_dir="/data/users/hgilmour/tb"


# Set up the output directory
OUTPUT_DIR="/data/users/hgilmour/initial_tracks/tobac_initial_tracks/lotus_output/feature_detection"
mkdir -p $OUTPUT_DIR

# Loop over the months
for month in ${months[@]}; do
    
    echo $year
    echo $month

    # Find the tracks files for the given month
    tb_file="tb_merge_${month}_${year}.nc"
    # construct the tracks path
    tb_path=${base_dir}/${tb_file}

    # Set up the output files
    OUTPUT_FILE="$OUTPUT_DIR/all_feature_detection.$month.$year.out"
    ERROR_FILE="$OUTPUT_DIR/all_feature_detection.$month.$year.err"

    # submit the batch job
    sbatch --mem=100000 --ntasks=4 --time=40 --output=$OUTPUT_FILE --error=$ERROR_FILE $EXTRACTOR $tb_path
    
done

