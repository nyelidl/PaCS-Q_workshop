# Workflow for tutorial

## Tutorial preparation

### Prerequisites software 
[UCSF chimerax](https://www.cgl.ucsf.edu/chimerax/)  
[VMD](https://www.ks.uiuc.edu/Research/vmd/)  
[Amber22 or later](https://ambermd.org/AmberMD.php)  
[]() 

For Windows users:  
[Discovery studio](https://www.3ds.com/products/biovia/discovery-studio)   
[MobaXterm](https://mobaxterm.mobatek.net/)   
[notepad++](https://notepad-plus-plus.org/)   
  
For Macbook users:   
[gaussview](https://gaussian.com/gaussview6/)   

### conda & PaCS-Q installation
`wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh`

`bash Miniconda3-latest-Linux-x86_64.sh`

`source ./miniconda3/etc/profile.d/conda.sh`

`conda create -n pacsq_env python=3.10`

`conda activate pacsq_env`

`pip install PaCS-Q`

formal information

`pacs_q -h`


## 1. System Preparation

1. **Download PDB file**  
   Download the structure file with PDB ID [3TD8](https://www.rcsb.org/structure/3DT8) .

2. **Residue Mutation**(notepad++ or vim)
   Change residue 47 from SGB to SER.
   <img width="2688" height="1601" alt="アセット 1" src="https://github.com/user-attachments/assets/6f1c1ea3-e7c3-4d5f-9967-b31d8e1d954a" />


3. **assigning Protonation state to protein**
   Process the structure using [pdb2pqr](https://server.poissonboltzmann.org/pdb2pqr).

4. **Run pdb4amber**  
   Standardize and sort the PDB file using pdb4amber.  
   `pdb4amber -i xxx.pqr -p input_pqr.pdb`  
   Do not forget to run `module load amber/22u23` first.

5. **Obtain the structure of sarin**  
   [sarin](https://pubchem.ncbi.nlm.nih.gov/compound/Sarin)  
   Convert the sdf format to pdb format by [Multiwfn](http://sobereva.com/multiwfn/) or [Openbabel](https://openbabel.org/index.html).  
   The converted file can be found [here](parameterization/sarin.pdb).  

6. **Import Ligand into PDB**  
   Merge the ligand structure into the protein (pdb file).  
   ```bash
   cat input_pqr.pdb sarin.pdb > input.pdb
   ```  

7. **Ligand Force Field Preparation**  
   Use antechamber to process the sarin and generate force field parameters.
    ```bash
    antechamber -i sarin.pdb -fi pdb -o MOL.mol2 -fo mol2 -c bcc -nc 0 -rn MOL -pf y                                          
    ```
    For your future research, I recommend using Gaussian16 or Gaussian25 (at the end of this year) to fit RESP charges.
   
8. **Adjust Ligand Position (chimeraX or discovery studio)**  
   Manually adjust the position of the ligand as needed.


## 2. System Building and MD Simulation in Amber

1. **Build System with LEaP**  
   Build the system using `tleap -f leap.in`
    
    [leap.in](parameterization/leap/leap.in):  
    ```bash
    source leaprc.protein.ff14SB
    source leaprc.gaff2
    source leaprc.water.tip3p
    
    MOL = loadmol2 MOL.mol2
    
    p = loadpdb input.pdb
    
    solvateBox p TIP3PBOX 14.0 iso
    addIons p Na+ 0
    saveamberparm p complex.top complex.crd
    quit
    ```
    `tleap -f leap.in`

2. **Minimization and Heating up the system**  
   make a run script (example: sub.sh):  
   
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
    
    inp=complex
    
    #minimization
    pmemd.cuda -O -i ./input/minWAT.in -o minWAT.out -p $inp.top -c $inp.crd -r minWAT.crd -ref $inp.crd
    
    pmemd.cuda -O -i ./input/minALL.in -o minALL.out -p $inp.top -c minWAT.crd -r minALL.crd -ref minWAT.crd
    
    #Heating up
    pmemd.cuda  -O -i ./input/md1.in -o md1.out -p $inp.top -c minALL.crd -ref minALL.crd -r md1.restrt -x md1.nc -v mdvel
   ```
   `sbatch sub.sh`  


3. **Run LB-PaCS MD via PaCS-Q**  
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
      conda activate pacsq_env
      pacs_q_md -cy 50 -cd 5 -s "resname MOL and name O1 O2" -s2 "resid 43 and name OG"
      ```

## 3. QM/MM Preparation and Execution

1. **Export Structures from LB-PaCS MD**  
   Export the desired structures from the LB-PaCS MD simulation.

2. **Prepare Reference Structure**  
   Create a reference structure file.  
   I. By Discovery Studio  
   
   https://github.com/user-attachments/assets/99123d9b-9e47-496e-a3af-d3a9aa0da5f2

   II. By gaussview
   

4. **Prepare QM/MM Input File**  
   Prepare the QM/MM input file (e.g., `qmmm.in`).
    ```
    Short QM/MM simulation
    &cntrl
    imin=0, nstlim=5,
    ntx=1,
    irest=0,
    dt=0.001,
    ntt=3, tempi=400.0, temp0=400.0,
    gamma_ln=2,
    ntb=2, ntp=1,
    cut=6.0,
    ntpr=1,
    ntwx=1,
    ntwr=100,
    pres0=1.0,
    barostat=1,
    ig=-1,
    ifqnt=1
    /
    &qmmm
    qmmask=':43,191',
    qmcharge=0,
    qm_theory='PM6-D',
    qmcut=6,
    qmshake=0,
    writepdb=1,
    /
    ```

6. **Run PaCS-Q**  
   Execute PaCS-Q for QM/MM simulation.
    ```
    #!/bin/bash
    #SBATCH --job-name=test_job
    #SBATCH --ntasks=8
    #SBATCH --mem=4GB
    #SBATCH --time=10:00:00
    #SBATCH --partition=active       
    #SBATCH --qos=cpu
    #SBATCH --account=workshop       
    
    module load amber/22
    source /data/home/training025/miniconda3/etc/profile.d/conda.sh
    conda activate pacsq
    ```
