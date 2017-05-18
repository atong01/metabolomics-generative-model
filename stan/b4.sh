#!/bin/bash
#SBATCH --partition=batch
#SBATCH -c 4 
#SBATCH --mem-per-cpu=32000
#SBATCH --time 47:30:00
#SBATCH --output=b4.%j.out
#SBATCH --error=b4.%j.err
python run2.py model_simple.stan 4 100000
