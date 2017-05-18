#!/bin/bash
#SBATCH --partition=batch
#SBATCH -c 8
#SBATCH --mem-per-cpu=24000
#SBATCH --time 47:30:00
#SBATCH --output=b7.%j.out
#SBATCH --error=b7.%j.err
python run3.py model_continuous.stan 8 2000 -p 10
python run3.py model_continuous.stan 8 2000 -p 20
python run3.py model_continuous.stan 8 2000 -p 30
