# Molecular Simulation Workflow

## 1. Structure Preparation

1. **Download PDB file**  
   Download the structure file with PDB ID `3DT8`.

2. **Residue Mutation**  
   Change residue 47 from SGB to SER.

3. **Run pdb2pqr**  
   Process the structure using pdb2pqr.

4. **Residue Name Correction**  
   Change all ASH residues to ASP.

5. **Run pdb4amber**  
   Standardize and sort the PDB file using pdb4amber.

6. **Ligand File Preparation**  
   Use antechamber to process the sarin pdb file and generate force field parameters.

7. **Import Ligand into PDB**  
   Merge the ligand structure into the main PDB file.

8. **Adjust Ligand Position**  
   Manually adjust the position of the ligand as needed.

## 2. System Building and MD Simulation in Amber

9. **Build System with LEaP**  
   Build the system using `tleap -f leap.in`.

10. **Run LB-PaCS MD via PaCS-Q**  
    Run LB-PaCS MD simulation using PaCS-Q.

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

