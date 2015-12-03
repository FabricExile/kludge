#!/bin/bash

set -ve

for d in tests/*; do
  [ ${d: -5} == ".skip" ] && continue
  
  EXTNAME=$(basename $d)
  INPUTS=$(ls $d/*.hpp | sort)

  ./kludge \
    --outdir=$d \
    --basename=actual \
    $EXTNAME \
    $INPUTS

  # clang-format --style=Google -i $d/actual.cpp

  scons -C "$d"

  FABRIC_EXTS_PATH=$d kl $d/test.kl
done
