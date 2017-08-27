#!/bin/bash

#SBATCH -J "TeamAwesome"
#SBATCH --output=logs/filedir%A.log
#SBATCH --partition=levque
#SBATCH --reservation=reserva-astro
#SBATCH --mem 2400

#load all libraries
module load astro

#run python script
python -W ignore Feature_Extractor.py $1

#Make sure that the script has finished
echo "Analysis completed."
