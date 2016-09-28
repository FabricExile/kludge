
## Quickstart

1. Download and unpack custom Clang build

```
cd ~
wget http://dist.fabric-engine.com/llvm/fabric-llvm-3.9-linux-x86_64-gcc_48.tar.bz2
tar jxf fabric-llvm-3.9-linux-x86_64-gcc_48.tar.bz2
```

1. Install pre-requisite Python modules:

```
pip install jinja2 pyparsing
```

1. Set up environment:

```
export KLUDGE_LLVM_ROOT="~/fabric-llvm-3.9-linux-x86_64-gcc_48"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$KLUDGE_LLVM_ROOT/lib" # if Clang is installed elsewhere
```

1. Validate that unit tests are passing:

```

1. View command-line help:

```
./kludge --help
```
