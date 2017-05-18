#!/bin/bash
#SBATCH --partition=batch
#SBATCH -c 8
#SBATCH --mem-per-cpu=24000
#SBATCH --time 47:30:00
#SBATCH --output=b8.%j.out
#SBATCH --error=b8.%j.err
python run3.py model_simple.stan 8 2000 -p 10
python run3.py model_simple.stan 8 2000 -p 20
python run3.py model_simple.stan 8 2000 -p 30
