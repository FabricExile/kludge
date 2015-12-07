#!/bin/bash

set -ve

for d in tests/*; do
  
  EXTNAME=$(basename $d)
  if [ -n "$1" ]; then
    [ "$1" != "$EXTNAME" ] && continue
  else
    [ -f "$d/skip" ] && continue
  fi

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
