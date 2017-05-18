#!/bin/bash
#SBATCH --partition=batch
#SBATCH -c 8 
#SBATCH --mem-per-cpu=2000
#SBATCH --time 01:30:00
#SBATCH --output=test.%N.%j.out
#SBATCH --error=test.%N.%j.err
python run_test.py 8 10000
