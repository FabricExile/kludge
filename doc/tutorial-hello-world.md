# Tutorial: Hello, World!

This section walks you through a first use case for Kludge.  We call this the "Hello World!" example because that's what the first example is always called, but we are actually doing something more interesting than simply saying "Hello, World!": we will wrap a simple C++ function in KL that actually takes and returns values.

Begin by creating a very simple C++ header file `Tutorial.hpp`:

```
#pragma once

int AddTwoInts(int lhs, int rhs);
```

and the corresponding source file `Tutorial.cpp`:

```
#include "Tutorial.hpp"

int AddTwoInts(int lhs, int rhs)
{
  return lhs + rhs;
}
```

Compile this library with the command:

```
g++ -fPIC -shared Tutorial.cpp -o libTutorial.so
```

Now, use Kludge's discover tool to build an API description of the library:

```
path/to/kludge discover Tutorial Tutorial.hpp
```

It will create three files: `Tutorial.decls.kludge.py` which consist of type declarations; `Tutorial.defns.kludge.py` which consists of member and method definitions; and `Tutorial.kludge.py` which specifies header files that must be included and incldues the other two files.  Take a look at each of these files.  `Tutorial.decls.kludge.py` should be empty (or rather, contain only comments); `Tutorial.defns.kludge.py` contains one non-comment line that describes the function:

```
ext.add_func('AddTwoInts', 'int', [Param('lhs', 'int'), Param('rhs', 'int')])
```

The description is meant to be human-readable because in more complex cases you may need to modify the descriptions produced by `kludge discover`.

We will now produce the actual KL extension.  Use the `kludge generate` tool to generate the extension code:

```
path/to/kludge generate Tutorial Tutorial.kludge.py
```

This command will process the input files and produce several output files. They are:

`Tutorial.kl`:
  The KL extension 'header' file that provides the types, functions and methods for KL

`Tutorial.cpp`:
  The C++ code that is called from the KL extension.  This is the C++ code that wraps the library, converting the C++ API into a KL API.

`Tutorial.fpm.json`:
  The KL extension manifest, as is always required for KL extensions.

`Tutorial.SConstruct`:
  The `scons` build script for the extension.

`Tutorial.test.{kl,out,py}`:
  Unit tests for the extension.  Ignore for now.

You should example `Tutorial.kl`.  There are a bunch of comments and some additional definitions, but the "meat" of the file is the code:

```
SInt32
AddTwoInts(
    SInt32 lhs,
    SInt32 rhs
    ) = "Tutorial_AddTwoInts_c03059fc730d732cfde6e83950379548";
```

This specifies a KL function that is implemented by C++ code in the extension DLL.  Next, look at `Tutorial.cpp`.  Again, there are a bunch of comments and extra definitions but the "meat" is the definition of the `AddTwoInts` function.

Let's try to compile the extension.  Run:

```
scons -f Tutorial.SConstruct
```

The compilation should work.  Now let's try to use the function in KL.  Create the file `test.kl` containing:

```
require Tutorial;
operator entry() {
  report(AddTwoInts(2,2));
}
```

then run:

```
FABRIC_EXTS_PATH=. kl test.kl
```

You will see that the extension cannot be loaded because there is a symbol error.  This is because `kludge generate` needs to be told that the library the extension depends on must be loaded.  Do this by adding the following lines anywhere in `Tutorial.kludge.py`:

```
ext.add_lib_dir('.')
ext.add_lib('Tutorial')
```

Regenerate and rebuild the extension, and then run KL again:

```
path/to/kludge generate Tutorial Tutorial.kludge.py
scons -f Tutorial.SConstruct
FABRIC_EXTS_PATH=. kl test.kl
```

The extension should now successfully load and you will see the correct result `4` as the last line.

Next: [Wrapping a Type](tutorial-wrapping-a-type.md)
