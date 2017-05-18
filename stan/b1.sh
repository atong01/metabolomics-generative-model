#!/bin/bash
#SBATCH --partition=batch
#SBATCH -c 32
#SBATCH --mem-per-cpu=8000
#SBATCH --time 47:30:00
#SBATCH --output=b1.%j.out
#SBATCH --error=b1.%j.err
python run2.py model_simple.stan 32 6000
