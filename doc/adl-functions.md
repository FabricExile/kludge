# Wrapping Functions

It has already been shown in the tutorial how to wrap functions.  The specific method that is called is `ext.add_func()` (or `ns.add_func()` for [namespaces](adl-namespaces.md)).  It takes the parameters:

```
  def add_func(self, cpp_name, returns=None, params=[], kl_name=None):
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

The result of `add_method()` supports `add_comment(comment)` and `add_test(kl, out)`.

- `add_comment(comment)` adds a comment that will appear, verbatim, above the KL wrapping for the function.  The comment must include KL commenting delimiters.  This is used by `kludge discover` to bring C++ function comments into KL.

- `add_test(kl, out)` adds a unit test; it takes the `kl` parameter which is KL code for the test, and the `out` parameter which is the expected output for the test.  See [Adding Unit Tests](unit-tests.md) for more details.

Next: [Wrapping Types](adl-types.md)
