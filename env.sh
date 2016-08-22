# libclang
#export LLVM_PATH="/build/llvm-3.8/build"
export LLVM_PATH="/build/fabric-llvm/build"
export PATH="$PATH:/opt/usd-deps/bin:$LLVM_PATH/bin"
export PYTHONPATH="$PYTHONPATH:$LLVM_PATH/../tools/clang/bindings/python"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/opt/usd-deps/lib:/opt/gcc-4.8/lib64:$LLVM_PATH/lib"

# Bullet
export BULLET_DIR=/build/arbus/ThirdParty/PreBuilt/Linux/x86_64/Debug/bullet/2.78
#export BULLET_DIR=/home/andrew/foo/bullet

# USD
export USD_INSTALL_ROOT=/opt/pixar/usd
export PATH=$PATH:$USD_INSTALL_ROOT/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$USD_INSTALL_ROOT:$USD_INSTALL_ROOT/lib:$USD_INSTALL_ROOT/packages/openexr-2.1.0/lib
export PYTHONPATH=$PYTHONPATH:$USD_INSTALL_ROOT/lib/python
