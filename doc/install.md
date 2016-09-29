# Installation

The major ingredients to use Kludge are:

- An installation of Fabric Engine 2.4.0 or greater
- A build of LLVM/Clang that contains a custom version of the libclang Python module.
- Several additional (stock) Python modules that are used by Kludge

# System Requirements

Currently, Kludge only runs on 64-bit Linux but there are plans to support 64-bit Windows and OS X in the future.  Furthermore, you must have a GCC 4.8.x toolchain installed on the machine (usually in `/opt/gcc-4.8` if it is not already the system compiler).

## Installation Steps

1. Download and unpack Fabric Engine from [](http://dist.fabric-engine.com/FabricEngine/)

2. Download and unpack the custom build of LLVM/Clang from [](http://dist.fabric-engine.com/llvm/):

  ```
  cd ~
  wget http://dist.fabric-engine.com/llvm/fabric-llvm-3.9-linux-x86_64-gcc_48.tar.bz2
  tar jxf fabric-llvm-3.9-linux-x86_64-gcc_48.tar.bz2
  ```

3. Install pre-requisite Python modules:

  ```
  pip install jinja2 pyparsing scons pytest pytest-xdist
  ```

## Running Kludge

1. Set up Fabric environment:

  ```
  source path/to/fabric/environment.sh
  ```

2. Set up Kludge environment:

  ```
  export KLUDGE_LLVM_ROOT="~/fabric-llvm-3.9-linux-x86_64-gcc_48"
  export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$KLUDGE_LLVM_ROOT/lib" # if Clang is installed elsewhere on the system
  ```

If GCC 4.8 is not your default compiler then you will also need to add it to `LD_LIBRARY_PATH`:

  ```
  export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/opt/gcc-4.8/lib64"
  ```

3. Validate that kludge will run:

  ```
  ./kludge
  ```

You should see some help text.

4. Validate that unit tests are passing:

  ```
  py.test -n8
  ```

You should see no test failures.

[Next: Tutorial: Hello World](tutorial-hello-world.md)
