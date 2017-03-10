.. _KludgeTutorialHelloWorld:

Tutorial: Hello, World!
==============================

This section walks you through a first use case for Kludge.  We call this the "Hello World!" example because that's what the first example is always called, but we are actually doing something more interesting than simply saying "Hello, World!": we will wrap a simple C++ function in KL that actually takes and returns values.

Begin by creating a very simple C++ header file :file:`Tutorial.hpp`:

.. code-block:: c++
  :caption: Tutorial.hpp

  #pragma once

  int AddTwoInts(int lhs, int rhs);

and the corresponding source file :file:`Tutorial.cpp`:

.. code-block:: c++
  :caption: Tutorial.cpp

  #include "Tutorial.hpp"

  int AddTwoInts(int lhs, int rhs)
  {
    return lhs + rhs;
  }

Compile this library with the command:

.. code-block:: console

  $ g++ -fPIC -shared Tutorial.cpp -o libTutorial.so

Now, use Kludge's discover tool to build an API description of the library:

.. code-block:: console

  $ kludge discover Tutorial Tutorial.hpp

It will create three files: :file:`Tutorial.decls.kludge.py` which consist of type declarations; :file:`Tutorial.defns.kludge.py` which consists of member and method definitions; and :file:`Tutorial.kludge.py` which specifies header files that must be included and incldues the other two files.  Take a look at each of these files.  :file:`Tutorial.decls.kludge.py` should be empty (or rather, contain only comments); :file:`Tutorial.defns.kludge.py` contains one non-comment line that describes the function:

.. code-block:: python

  ext.add_func('AddTwoInts', 'int', [Param('lhs', 'int'), Param('rhs', 'int')])

The description is meant to be human-readable because in more complex cases you may need to modify the descriptions produced by ``kludge discover``.

We will now produce the actual KL extension.  Use the ``kludge generate`` tool to generate the extension code:

.. code-block:: console

  kludge generate Tutorial Tutorial.kludge.py

This command will process the input files and produce several output files. They are:

:file:`Tutorial.kl`:
  The KL extension 'header' file that provides the types, functions and methods for KL

:file:`Tutorial.cpp`:
  The C++ code that is called from the KL extension.  This is the C++ code that wraps the library, converting the C++ API into a KL API.

:file:`Tutorial.fpm.json`:
  The KL extension manifest, as is always required for KL extensions.

:file:`Tutorial.SConstruct`:
  The ``scons`` build script for the extension.

:file:`Tutorial.test.kl`, :file:`Tutorial.test.out`, :file:`Tutorial.test.py`:
  Unit tests for the extension.  You can safely ignore these for now, but see :ref:`KludgeUnitTests` for more details.

Please look at :file:`Tutorial.kl`.  There are a bunch of comments and some additional definitions, but the "meat" of the file is the code:

.. code-block:: kl

  SInt32
  AddTwoInts(
      SInt32 lhs,
      SInt32 rhs
      ) = "Tutorial_AddTwoInts_c03059fc730d732cfde6e83950379548";

This specifies a KL function that is implemented by C++ code in the extension DLL.  Next, look at :file:`Tutorial.cpp`.  Again, there are a bunch of comments and extra definitions but the "meat" is the definition of the ``AddTwoInts`` function.

Let's try to compile the extension.  Run:

.. code-block:: console

  $ scons -f Tutorial.SConstruct

The compilation should work.  Now let's try to use the function in KL.  Create the file :file:`test.kl` containing:

.. code-block:: kl

  require Tutorial;
  operator entry() {
    report(AddTwoInts(2,2));
  }

then run:

.. code-block:: console

  $ FABRIC_EXTS_PATH=. kl test.kl

You will see that the extension cannot be loaded because there is a symbol error.  This is because ``kludge generate`` needs to be told that the library the extension depends on must be loaded.  Do this by adding the following lines anywhere in :file:`Tutorial.kludge.py`:

.. code-block:: python

  ext.add_lib_dir('.')
  ext.add_lib('Tutorial')

This is one of the reasons that ``kludge discover`` and ``kludge generate`` are separate steps: it's not possible to know from the C++ header files what libraries are needed to compile and link the extension.  For more information on methods that affect compilation, see :ref:`KludgeADLCompMethods`.

Regenerate and rebuild the extension, and then run KL again:

.. code-block:: console

  $ kludge generate Tutorial Tutorial.kludge.py
  $ scons -f Tutorial.SConstruct
  $ FABRIC_EXTS_PATH=. kl test.kl

The extension should now successfully load and you will see the correct result ``4`` as the last line.
