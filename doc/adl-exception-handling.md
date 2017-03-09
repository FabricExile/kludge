# Exception Handling

To handle exception coming from the source API you can use the so called `exception prolog` and `exception epilog`. The exception prolog and epilog are used for all functions and methods in the C++ code and allow you to catch exeptions. Make sure to only catch the typed exceptions thrown by the source API though.

```
  ext.set_cpp_exception_prolog(
    self,
    exception_prolog
    )
```

`exception_prolog` is the C++ code to place prior to the function / method invocation.

```
  ext.set_cpp_exception_epilog(
    self,
    exception_epilog
    )
```

`exception_epilog` is the C++ code to place after to the function / method invocation.

For example to catch a `std::runtime_error`:

```
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
```

Next: [Pointers and References](ptrs_refs.md)
