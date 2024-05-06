#!/bin/bash

#SBATCH --job-name=3d    # Job name
#SBATCH --mail-type=END,FAIL              # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=xin.ma@ufl.edu    # Where to send mail.  Set this to your email address
#SBATCH --ntasks=1                  # Number of MPI tasks (i.e. processes)
#SBATCH --cpus-per-task=1           # Number of cores per MPI task 
#SBATCH --nodes=1                    # Maximum number of nodes to be allocated
#SBATCH --ntasks-per-node=1         # Maximum number of tasks on each node
#SBATCH --mem-per-cpu=40gb          # Memory (i.e. RAM) per processor
#SBATCH --time=72:00:00              # Wall time limit (days-hrs:min:sec)
#SBATCH --output=./%x.log    # Path to the standard output and error files relative to the working directory


module load conda
conda activate /blue/li.chen1/xin.ma/conda/envs/maldi3d
cd /blue/li.chen1/xin.ma/sunlab/maldi/3d_maldi/github

python main.py
