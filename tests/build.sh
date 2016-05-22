dir="$1"
if [ -z "$dir" ]; then
  dir=$(pwd)
fi

KLUDGE="./kludge"
if [ ! -e "$KLUDGE" ]; then
  KLUDGE="../../kludge"
fi
if [ ! -e "$KLUDGE" ]; then
  echo "unable to find kludge"
  exit 1
fi

EXTNAME=$(basename $dir)

INPUTS=$(ls $dir/*.hpp $dir/*.h | sort)

MAYBE_CONFIG=
[ -f "$dir/config.json" ] && MAYBE_CONFIG="--config=$dir/config.json"

$KLUDGE \
  $MAYBE_CONFIG \
  --outdir=$dir \
  --basename=actual \
  $EXTNAME \
  $INPUTS

# clang-format --style=Google -i $dir/actual.cpp

scons -C "$dir"


