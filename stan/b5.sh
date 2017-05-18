#!/bin/bash
#SBATCH --partition=batch
#SBATCH -c 16
#SBATCH --mem-per-cpu=8000
#SBATCH --time 47:30:00
#SBATCH --output=b5.%j.out
#SBATCH --error=b5.%j.err
python run2.py model.stan 16 20000
