#!/bin/bash

inp=complex

#minimization
pmemd.cuda -O -i ./input/minWAT.in -o minWAT.out -p $inp.top -c $inp.crd -r minWAT.crd -ref $inp.crd

pmemd.cuda -O -i ./input/minALL.in -o minALL.out -p $inp.top -c minWAT.crd -r minALL.crd -ref minWAT.crd

#Heating up
pmemd.cuda  -O -i ./input/md1.in -o md1.out -p $inp.top -c minALL.crd -ref minALL.crd -r md1.restrt -x md1.nc -v mdvel

