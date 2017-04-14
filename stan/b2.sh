#!/bin/bash
#SBATCH --partition=largemem
#SBATCH -c 16
#SBATCH --mem-per-cpu=16000
#SBATCH --time 23:00:00
#SBATCH --output=results/run.%N.%j.out
#SBATCH --error=results/run.%N.%j.err
python run.py 16 200000
