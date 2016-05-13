LLVM_PATH="/build/llvm-3.8/build"
export PATH="$PATH:$LLVM_PATH/bin"
export PYTHONPATH="$PYTHONPATH:$LLVM_PATH/lib/python"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$LLVM_PATH/lib"

# Bullet
export BULLET_DIR=/build/arbus/ThirdParty/PreBuilt/Linux/x86_64/Release/bullet/2.78

# USD
export USD_INSTALL_ROOT=/opt/pixar/usd
export PATH=$PATH:$USD_INSTALL_ROOT/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$USD_INSTALL_ROOT:$USD_INSTALL_ROOT/lib:$USD_INSTALL_ROOT/packages/openexr-2.1.0/lib
export PYTHONPATH=$PYTHONPATH:$USD_INSTALL_ROOT/lib/python
