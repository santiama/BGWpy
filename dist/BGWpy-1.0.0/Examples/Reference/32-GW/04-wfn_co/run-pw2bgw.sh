#!/usr/bin/env bash

MPIRUN='mpirun -n 2 --npernode 2'
PW='pw.x'
PW_flags=''
PW2BGW='pw2bgw.x'


$MPIRUN $PW2BGW -in wfn.pp.in &> wfn.pp.out
