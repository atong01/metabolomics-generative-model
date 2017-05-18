#!/bin/bash
#SBATCH --partition=batch
#SBATCH -c 16
#SBATCH --mem-per-cpu=16000
#SBATCH --time 23:00:00
#SBATCH --output=b2.%j.out
#SBATCH --error=b2.%j.err
python run.py -d 16 10000
