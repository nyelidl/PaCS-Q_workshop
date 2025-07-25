#!/usr/bin/bash
cyc=10000
candi=5

for ((i=0; i<=cyc; i++)); do
    for ((j=1; j<=candi; j++)); do
            echo "trajin ../MDrun/$i/$j/md${i}_${j}.nc"
    done
done
