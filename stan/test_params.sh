#!/bin/bash
#SBATCH --partition=batch
#SBATCH -c 8 
#SBATCH --mem-per-cpu=2000
#SBATCH --time 01:30:00
#SBATCH --output=param_test.%N.%j.out
#SBATCH --error=param_test.%N.%j.err
python run_param_test.py 8 10000 0.01 0.01
python run_param_test.py 8 10000 1.0 0.01
python run_param_test.py 8 10000 1.0 0.1
python run_param_test.py 8 10000 1.0 1.0
python run_param_test.py 8 10000 0.1 0.01
python run_param_test.py 8 10000 0.01 1
