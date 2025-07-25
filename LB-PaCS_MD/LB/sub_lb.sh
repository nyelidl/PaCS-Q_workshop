#!/bin/bash
#SBATCH --job-name=PaCSQ            
#SBATCH --ntasks=4                  
#SBATCH --time=24:00:00             
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=6           
#SBATCH --mem=10GB                 
#SBATCH --partition=active        

module load amber/22
source /data/home/hmahedi/miniconda3/bin/activate
conda activate pacsq
python3 /data/home/hmahedi/Workshop_PaCS_Q/PaCS-Q/PaCSQ_for_workshop/pacsq_toolkit/pacs_q_md.py -cy 50 -cd 5 -s "resname MOL and name O1 O2" -s2 "resid 43 and name OG"

