#!/bin/bash
#SBATCH --mem=100000
#SBATCH --ntasks=4
#SBATCH --time=40

#Extract args from command line
tb_file=$1

# Print the tracks file
echo "$tb_file"

# Run the unique_cells.py script
python feature_detection.py ${tb_file}