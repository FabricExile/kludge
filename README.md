# Kludge README.md

Kludge is a tool to generate KL extensions that wrap C++ libraries.

## License

Kludge is licensed under a 3-clause BSD license.  See LICENSE.txt for details.

## Quickstart

Download and unpack custom Clang build

```
cd ~
wget http://dist.fabric-engine.com/llvm/fabric-llvm-3.9-linux-x86_64-gcc_48.tar.bz2
tar jxf fabric-llvm-3.9-linux-x86_64-gcc_48.tar.bz2
```

Install pre-requisite Python modules:

```
pip install jinja2 pyparsing pytest pytest-xdist
```

Set up environment:

```
export KLUDGE_LLVM_ROOT="~/fabric-llvm-3.9-linux-x86_64-gcc_48"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$KLUDGE_LLVM_ROOT/lib" # if Clang is installed elsewhere
```

Validate that unit tests are passing:

```
py.test -n8
```

View command-line help:

```
./kludge --help
```

## Documentation

Documentation can be found under [doc/](doc/).
