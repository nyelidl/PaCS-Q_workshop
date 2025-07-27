# Workflow for tutorial

## Tutorial preparation

## Prerequisites software 
[UCSF chimerax](https://www.cgl.ucsf.edu/chimerax/)  
[VMD](https://www.ks.uiuc.edu/Research/vmd/)  
[Amber22 or later](https://ambermd.org/AmberMD.php)  
[]() 

For Windows users:  
[Discovery studio](https://www.3ds.com/products/biovia/discovery-studio)   
[MobaXterm](https://mobaxterm.mobatek.net/)   
[notepad++](https://notepad-plus-plus.org/)   


### conda installation
`wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh`

`bash Miniconda3-latest-Linux-x86_64.sh`

`source ./miniconda3/etc/profile.d/conda.sh`

`conda create -n PaCS-Q python=3.10`

`conda activate PaCS-Q`

`pip install PaCS-Q`

formal information

`pacs_q -h`


## 1. System Preparation

1. **Download PDB file**  
   Download the structure file with PDB ID `3DT8` (link).

2. **Residue Mutation**  
   Change residue 47 from SGB to SER. (add how to picture)

3. **assigning Protonation state to protein**  
   Process the structure using pdb2pqr.

4. **Run pdb4amber**  
   Standardize and sort the PDB file using pdb4amber.

5. **Ligand Force Field Preparation**  
   Use antechamber to process the sarin and generate force field parameters. (add command line)

6. **Import Ligand into PDB**  
   Merge the ligand structure into the protein (pdb file). cat command line

7. **Adjust Ligand Position (chimeraX or discovery studio)**  
   Manually adjust the position of the ligand as needed.

## 2. System Building and MD Simulation in Amber

8. **Build System with LEaP**  
   Build the system using `tleap -f leap.in`

   detail of leap.in

9. **Minization and Heating up the system**  


10. **Run LB-PaCS MD via PaCS-Q**  (how to check the result, or excel)
    Run LB-PaCS MD simulation using PaCS-Q
    submit by sbatch
    
      ```bash
      #!/bin/bash
      #SBATCH --job-name=test_job
      #SBATCH --ntasks=1
      #SBATCH --cpus-per-task=1
      #SBATCH --mem=4GB
      #SBATCH --time=01:00:00
      #SBATCH --partition=active       
      #SBATCH --qos=normal            
      #SBATCH --account=workshop       
      #SBATCH --gres=gpu:1             
      
      module load amber/22
      source /data/home/training025/miniconda3/etc/profile.d/conda.sh
      conda activate pacsq
      pacs_q_md -cy 50 -cd 5 -s "resname MOL and name O1 O2" -s2 "resid 43 and name OG"
      ```

## 3. QM/MM Preparation and Execution

1. **Export Structures from LB-PaCS MD**  
   Export the desired structures from the LB-PaCS MD simulation.

2. **Prepare Reference Structure**  
   Create a reference structure file.
   I. By Discovery Studio
   
   https://github.com/user-attachments/assets/99123d9b-9e47-496e-a3af-d3a9aa0da5f2



4. **Prepare QM/MM Input File**  
   Prepare the QM/MM input file (e.g., `qmmm.in`).

5. **Run PaCS-Q**  
   Execute PaCS-Q for QM/MM simulation.

