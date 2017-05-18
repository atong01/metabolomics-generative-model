#!/bin/bash
#SBATCH --partition=batch
#SBATCH -c 16 
#SBATCH --mem-per-cpu=12000
#SBATCH --time 47:30:00
#SBATCH --output=b3.%j.out
#SBATCH --error=b3.%j.err
python run.py -d 16 50000
