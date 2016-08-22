# libclang
export KLUDGE_LLVM_ROOT="/build/fabric-llvm/install"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/opt/usd-deps/lib:/opt/gcc-4.8/lib64:$KLUDGE_LLVM_ROOT/lib"

# Bullet
export BULLET_DIR=/build/arbus/ThirdParty/PreBuilt/Linux/x86_64/Debug/bullet/2.78
#export BULLET_DIR=/home/andrew/foo/bullet

# USD
export USD_INSTALL_ROOT=/opt/pixar/usd
export PATH=$PATH:$USD_INSTALL_ROOT/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$USD_INSTALL_ROOT:$USD_INSTALL_ROOT/lib:$USD_INSTALL_ROOT/packages/openexr-2.1.0/lib
export PYTHONPATH=$PYTHONPATH:$USD_INSTALL_ROOT/lib/python
