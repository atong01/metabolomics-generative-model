#!/bin/bash
#SBATCH --partition=batch
#SBATCH -c 8 
#SBATCH --mem-per-cpu=4000
#SBATCH --time 02:30:00
#SBATCH --output=run_long.%N.%j.out
#SBATCH --error=run_long.%N.%j.err
python run.py 8 100000
