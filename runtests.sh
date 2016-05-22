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

  ./tests/build.sh $d
  ./tests/run.sh $d
done
