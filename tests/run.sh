dir="$1"
if [ -z "$dir" ]; then
  dir="."
fi
FABRIC_EXTS_PATH=$dir kl $dir/test.kl
