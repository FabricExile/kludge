#!/bin/bash

set -ve

for d in tests/*; do

  if [ ! -d "$d" ]; then
    continue
  fi
  
  EXTNAME=$(basename $d)
  if [ -n "$1" ]; then
    [ "$1" != "$EXTNAME" ] && continue
  else
    [ -f "$d/skip" ] && continue
  fi

  INPUTS=$(ls $d/*.hpp $d/*.h | sort)

  MAYBE_CONFIG=
  [ -f "$d/config.json" ] && MAYBE_CONFIG="--config=$d/config.json"

  ./kludge \
    $MAYBE_CONFIG \
    --outdir=$d \
    --basename=actual \
    $EXTNAME \
    $INPUTS

  # clang-format --style=Google -i $d/actual.cpp

  scons -C "$d"

  FABRIC_EXTS_PATH=$d kl $d/test.kl
done
