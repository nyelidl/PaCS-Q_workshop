for i in A B C; do antechamber -i Lig${i}.mol2 -o Ligand${i}.mol2 -fi mol2 -fo mol2 -c bcc -pf yes -nc -2 -at gaff2 -j 5 -rn CH${i}; done
for i in A B C; do parmchk2 -i Ligand${i}.mol2 -f mol2 -o Ligand${i}.frcmod -s 2; done
