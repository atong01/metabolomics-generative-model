#!/bin/bash
#SBATCH --partition=batch
#SBATCH -c 8
#SBATCH --mem-per-cpu=24000
#SBATCH --time 47:30:00
#SBATCH --output=b6.%j.out
#SBATCH --error=b6.%j.err
python run2.py model_simple.stan 8 200000
