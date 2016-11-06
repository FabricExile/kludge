# Wrapping Functions and Function-Like Globals

It has already been shown in the tutorial how to wrap functions.  The specific method that is called is `ext.add_func()` (or `ns.add_func()` for [namespaces](adl-namespaces.md)).  It takes the parameters:

```
  add_func(
    self,
    cpp_name,
    returns=None,
    params=[],
    opt_params=[],
    kl_name=None,
    )
```

`cpp_name` is the name of the C++ function.  `returns` is the C++ type that the function returns.  `params` is the list of parameters that the function takes; each element is either `Param(name, cpp_type_name)` or just a string, in which case it is just the C++ type name.  If provided, `kl_name` is the name for the function in KL, which is otherwise the same as `cpp_name`.

For example, the description language code:

```
ext.add_func('Interpolate', 'Vec3', [Param('lhs', 'Vec3'), 'Vec3', Param('amount', 'float')])
```

is wrapped in KL as:

```
Vec3 Interpolate(Vec3 lhs, Vec3 arg1, Float32 amount);
```

Note that both built-in and wrapped types can be used for parameters and the return value; however, types must be wrapped if they are used for wrapped functions.  This is also true of [methods and other method-like additions to types](adl-methods.md).

The result of `add_func()` supports `add_comment(comment)` and `add_test(kl, out)`.

- `add_comment(comment)` adds a comment that will appear, verbatim, above the KL wrapping for the function.  The comment must include KL commenting delimiters.  This is used by `kludge discover` to bring C++ function comments into KL.

- `add_test(kl, out)` adds a unit test; it takes the `kl` parameter which is KL code for the test, and the `out` parameter which is the expected output for the test.  See [Adding Unit Tests](unit-tests.md) for more details.


Additional methods exist to wrap *function-like globals*, such as binary operator overloads that are external to class definitions.  The result of each of these support `add_comment(comment)` and `add_test(kl, out)`.  They are:

```
  add_bin_op(
    self,
    op,
    returns,
    params,
    ):
```

Wraps a global (external to a class definition) binary operator overload.  `op` is the operator itself, such as `+`, `-`, etc.

Next: [Wrapping Types](adl-types.md)
