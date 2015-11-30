#!/bin/bash

set -ve

for d in Tests/*; do
  EXTNAME=$(basename $d)
  INPUTS=$(ls $d/*.hpp | sort)
  python kludge.py \
    --outdir=$d \
    --basename=actual \
    $EXTNAME \
    $INPUTS
done
