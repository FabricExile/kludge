# Methods that Affect Compilation

You saw in the tutorials that you needed to add `ext.add_lib_dir()` and `ext.add_lib()` calls to the `.kludge.py` file in order to get one of the tutorial extensions to load.  Kludge has several methods to support compilation and linking that are described below.

## `ext.add_cpp_flag(cpp_flag)`

Adds a flag that is passed to the C++ compiler when the extension's C++ code is compiled.

## `add_cpp_define(cpp_define)`

Adds a C++ preprocessor definition that is passed to the C++ compile (the `-D` parameter in GCC and Clang)

## `ext.add_cpp_include_dir(directory)`

Adds an include directory to to the C++ include directory path (the `-I` parameter in GCC and Clang).

## `add_cpp_quoted_include(filepath)`

Adds a C++ inclusion directive to the top of the generated C++ extension.  The inclusion uses double quotes, ie. `#include "filepath"`

## `add_cpp_angled_include(filepath)`

Adds a C++ inclusion directive to the top of the generated C++ extension.  The inclusion uses angle brackets, ie. `#include <filepath>`

## `add_lib_dir(dirpath)`

Adds a library directory to the C++ lib directory path (the `-L` parameter in GCC and Clang)

## `add_lib(libname)`

Adds a library to the C++ link command (the `-l` parameters in GCC and Clang)

## `add_cpp_topmost(cpp_code)`

Adds verbatim C++ code above everything (except comments) at the top of the generated extension C++ file.  Useful for when you must define macros or perform inclusions before anything else is defined or included.

## `add_cpp_prolog(cpp_code)`

Adds verbatim C++ code near the top of the generated extension C++ file, right after the include statments from `add_cpp_quoted_include` and `add_cpp_angled_include`.

## `add_cpp_epilog(cpp_code)`

Adds verbatim C++ code at the bottom of the generated extension C++ file.

## `add_kl_require(kl_ext_name)`

Add a KL `require` statement for the given extension at the top of the generated extension KL file.

## `add_kl_prolog(kl_code)`

Adds verbatim KL code near the top of the generated extension KL file, right after the require statements

## `add_kl_epilog(kl_code)`

Adds verbatim KL code at the end of the generated extension KL file.

Next: [Pointers and References](ptrs_refs.md)
