# Installation

Kludge ships with Fabric Engine version 2.5.0.  However, additional Python modules must be installed before Kludge can be used.

## Installation Steps

1. Download and unpack Fabric Engine from [](http://dist.fabric-engine.com/FabricEngine/)

2. Install pre-requisite Python modules:

  ```
  pip install jinja2 pyparsing scons pytest pytest-xdist subprocess difflib
  ```

## Running Kludge

1. If you haven't already, set up a Fabric environment as described in the Fabric documentation.  For instance, on Linux systems this is often done throught the shell command:

  ```
  source path/to/fabric/environment.sh
  ```

2. Validate that Kludge will run:

  ```
  ./kludge
  ```

  You should see some help text.

3. Validate that the Kludge unit tests pass:

  ```
  py.test -n8 "$FABRIC_DIR/Test/Kludge"
  ```

  You should see no test failures.

Next: [Tutorial: Hello World](tutorial-hello-world.md)
