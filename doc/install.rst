.. _KludgeInstall:

Installation
========================

Kludge ships with Fabric Engine version 2.5.0.  However, additional Python modules must be installed before Kludge can be used.

Installation Steps
------------------------

1. Download and unpack Fabric Engine from http://dist.fabric-engine.com/FabricEngine/

2. Install pre-requisite Python modules.  On all platforms, install these modules:

  .. code-block:: console
  
    $ pip install jinja2 pyparsing scons pytest pytest-xdist

  Additionally, Linux and OS X require that you install a few more modules that are built-in on Windows:

  .. code-block:: console
  
    $ pip install subprocess difflib

Running Kludge
----------------------

1. If you haven't already, set up a Fabric environment as described in the Fabric documentation.  For instance, on Linux systems this is often done throught the shell command:

  .. code-block:: console
  
    $ source path/to/fabric/environment.sh

2. Validate that Kludge will run:

  .. code-block:: console
  
    $ kludge

  You should see some help text.

3. Validate that the Kludge unit tests pass:

  .. code-block:: console
  
    $ py.test -n8 "$FABRIC_DIR/Tests/Kludge"

  You should see no test failures.
