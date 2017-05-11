.. _KludgeADCompMethods

Methods that Affect Compilation
=================================================

You saw in the tutorials that you needed to add ``ext.add_lib_dir()`` and ``ext.add_lib()`` calls to the :file:`.kludge.py` file in order to get one of the tutorial extensions to load.  Kludge has several methods to support compilation and linking that are described below.

Methods that Affect the Generated Build Script
#####################################################

``ext.add_cpp_flag(cpp_flag)``
-----------------------------------------

Adds a flag that is passed to the C++ compiler when the extension's C++ code is compiled.

``add_cpp_define(cpp_define)``
-----------------------------------------

Adds a C++ preprocessor definition that is passed to the C++ compile (the ``-D`` parameter in GCC and Clang)

``ext.add_cpp_include_dir(directory)``
-----------------------------------------

Adds an include directory to the C++ include directory path (the ``-I`` parameter in GCC and Clang).

``add_lib_dir(dirpath)``
-----------------------------------------

Adds a library directory to the C++ lib directory path (the ``-L`` parameter in GCC and Clang)

``add_lib(libname)``
-----------------------------------------

Adds a library to the C++ link command (the ``-l`` parameters in GCC and Clang)

Methods that Affect Generated C++ Code
#####################################################

``add_cpp_quoted_include(filepath)``
-----------------------------------------

Adds a C++ inclusion directive to the top of the generated C++ extension.  The inclusion uses double quotes, i.e. ``#include "filepath"``

``add_cpp_angled_include(filepath)``
-----------------------------------------

Adds a C++ inclusion directive to the top of the generated C++ extension.  The inclusion uses angle brackets, i.e. ``#include <filepath>``

``add_cpp_topmost(cpp_code)``
-----------------------------------------

Adds verbatim C++ code above everything (except comments) at the top of the generated extension C++ file.  Useful for when you must define macros or perform inclusions before anything else is defined or included.

``add_cpp_prolog(cpp_code)``
-----------------------------------------

Adds verbatim C++ code near the top of the generated extension C++ file, right after the include statements from ``add_cpp_quoted_include`` and ``add_cpp_angled_include``.

``add_cpp_epilog(cpp_code)``
-----------------------------------------

Adds verbatim C++ code at the bottom of the generated extension C++ file.

``set_cpp_exception_prolog(exception_epilog)`` and ``set_cpp_exception_epilog(exception_epilog)``
-----------------------------------------------------------------------------------------------------------

To handle exception coming from the source API you can use the so called *exception prolog* and *exception epilog*. The exception prolog and epilog are used for all functions and methods in the C++ code and allow you to catch exeptions.  The prolog is placed at the beginning of the function and the epilog is placed at the end.

.. note:: Ensure to only catch the typed exceptions thrown by the source API!

For example to catch a ``std::runtime_error``:

.. code-block:: python

  ext.set_cpp_exception_prolog("""
  try
  {
  """)

  ext.set_cpp_exception_epilog("""
  }
  catch(std::runtime_error e)
  {
    std::string message = "Caught runtime_error: ";
    message += e.what();
    Fabric::EDK::throwException(message.c_str());
  }
  """)

Methods that Affect Generated KL Code
#####################################################

``add_kl_require(kl_ext_name)``
-----------------------------------------

Add a KL `require` statement for the given extension at the top of the generated extension KL file.

``add_kl_prolog(kl_code)``
-----------------------------------------

Adds verbatim KL code near the top of the generated extension KL file, right after the require statements

``add_kl_epilog(kl_code)``
-----------------------------------------

Adds verbatim KL code at the end of the generated extension KL file.

Methods that Affect the Generated Extension
#####################################################

``add_ext_version_spec(self, major=0, minor=0, revision=0)``
-------------------------------------------------------------

If present, sets the KL extension version for the generated extension.


Canvas-Related Methods
#####################################################

``add_dfg_presets_spec(preset_path, dir="DFG")``
------------------------------------------------------

Adds a Canvas preset spec to the generated :file:``<ExtName>.fpm.json`` file.  Note that this does not
actually generate the presets; instead, use the ``kl2dfg`` tool to generate the presets or create them manually.
