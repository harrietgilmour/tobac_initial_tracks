#!/bin/bash
#SBATCH --mem=100000
#SBATCH --ntasks=4
#SBATCH --time=40

#Extract args from command line
features_file=$1
tb_file=$2

# Print the tracks file
echo "$features_file"
echo "$tb_file"

# Run the unique_cells.py script
python tracking.py ${features_file} ${tb_file}