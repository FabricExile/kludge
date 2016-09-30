# Wrapping Methods and Method-Like Type Additions

When a type is wrapped using `ns.add_owned_type()`, `ns.add_in_place_type()` or `ns.add_wrapped_type()`, the result is a record object that can be used to add methods and the like to the type.  In addition to nested types, enums, and aliases, as described in the section on [namespaces](namespace.md), the following methods can be called to fill out the type:

## `add_member()`

The `add_member()` method adds a member to the type.  Its parameters are:

```
  def add_member(
    self,
    cpp_name,
    cpp_type_name,
    getter='',
    setter='',
    visibility=None,
    ):
```

`cpp_name` is the name of the member in C++; it will have the same name in KL.  `cpp_type_name` is the C++ type name of the member.  The `visibility`, if provided, is one of `Visibility.public`, `Visibility.protected` and `Visibility.private`; if not provided, it defaults to the current default visibility, which starts at `Visibility.public` but can be changed with `set_default_visibility()`.

Public members are accessed via getters and setters that are automatically built for the type. The name of the getter defaults to `cxxGet_<memberName>` and the setter to `cxxSet_<memberName>` but can be controlled with the corresponding parameter.  If either `getter` or `setter` is set to `None`, the getter or setter will be completely omitted.

It is not required to specify the members for a type, except when using in-place type wrapping; if not specified, the members will simply not be accessible from KL.

Note that for in-place types the members can also be accessed directly from KL.

## `add_method()`

The `add_method()` method adds a method the type.  It takes the parameters:

```
  def add_method(
    self,
    name,
    returns=None,
    params=[],
    opt_params=[],
    this_access=ThisAccess.const,
    kl_name=None,
```

The `name` is the name of the method in C++; `kl_name`, if present, is the name in KL, otherwise it will default to `name`.

The `returns` parameter is the C++ return type of the method.  If omitted or `None` it is treated as `void`.

The `this_access` parameter specifies what can be done with `this` for the method.  It can be `ThisAccess.static`, which corresponds to a C++ static method; `ThisAccess.const`, which corresponds to a C++ const method; or `ThisAccess.mutable` which corresponds to a default C++ method (neither static nor const).

`params` is the list of required parameters, and `opt_params` is the list of optional parameters; that is, the parameters that have default values in KL.  Each parameter is either a string, which is the C++ type of the parameter, or a value of type `Param(name, cpp_type_name)`, which also specifies the name of the parameter that appears in the C++ and KL code generated for the extension.

Optional parameters are handled by generating multiple copies of the method, one for each additional optional parameter.  For instance, the code:

```
ty = ext.add_owned_type('MyType')
ty.add_method('foo', 'float', ['int'], ['float', 'bool'], ThisAccess.mutable)
```

will generate three KL methods:

```
Float32 MyType.foo!(SInt32);
Float32 MyType.foo!(SInt32, Float32);
Float32 MyType.foo!(SInt32, Float32, Boolean);
```

Note that it is entirely possible to call `add_method` multiple times with the same name; the effect is C++ and KL method overloading (which work the same way).  However, if there is an exact match on parameter types then there will be a C++ compile error for the extension itself.

Static methods are wrapped as a global function with the method name prefixed by the type name.  So, for example,

```
ty.add_method('Bar', this_access=ThisAccess.static)
```

becomes:

```
MyType_Bar();
```

in KL.

The result of `add_method()` supports `add_comment(comment)` and `add_test(kl, out)`.

- `add_comment(comment)` adds a comment that will appear, verbatim, above the KL wrapping for the method.  The comment must include KL commenting delimiters.  This is used by `kludge discover` to bring C++ method comments into KL.

- `add_test(kl, out)` adds a unit test; it takes the `kl` parameter which is KL code for the test, and the `out` parameter which is the expected output for the test.

# `add_const_method()`, `add_mutable_method()` and `add_static_method()`

These are shortcuts for `add_method()` that specify the `ThisAccess` value as part of the method name.

## `add_ctor()`

The `add_ctor()` method adds a constructor for the type.  The parameters are:

```
  def add_ctor(self, params=[], opt_params=[]):
```

`params` and `opt_params` are as in `add_method()`.  The result of `add_ctor()` supports `add_comment(comment)` and `add_test(kl, out)`.

Example:

```
ty = ext.add_owned_type('MyType')
ty.add_ctor(['int'], ['float', 'bool'])
```

will generate three KL constructors:

```
MyType(SInt32);
MyType(SInt32, Float32);
MyType(SInt32, Float32, Boolean);
```

## `add_call_op()`

The `add_call_op()` method provides a wrapping for C++ `operator()`.  It takes the parameters:

```
  def add_call_op(
    self,
    returns=None,
    params=[],
    opt_params=[],
    this_access=ThisAccess.const,
    ):
```

All of the parameters work as for methods.  The result of `add_call()` supports `add_comment(comment)` and `add_test(kl, out)`.


The call operator is mapped into KL as a method `cxxCall`.  For instance, the wrapping:

```
ty.add_call_op('int', ['float'])
```

results in KL:

```
SInt32 MyType.cxxCall(Float32);
```

## `add_uni_op()`

The `add_uni_op()` method wraps a C++ unary operator `++` or `--`.  Its parameters are:

```
  def add_uni_op(
    self,
    op,
    returns,
    kl_method_name=None,
    ):
```

The `op` parameter is the name of the operator, either `++` or `--`.  The `returns` parameter is the C++ type name of the return value of the operator.  By default, the operator will be mapped as a KL method `cxxInc` or `cxxDec`, but this can be controlled with the `kl_method_name` parameter.  The result of `add_uni_op()` supports `add_comment(comment)` and `add_test(kl, out)`.

Note that, currently, Kludge only supports overloads of **prefix** `++` and `--`.

Example:

```
ty.add_uni_op('++', 'int');
```

Results in:

```
SInt32 MyType.cxxInc!();
```

## `add_bin_op()`

The `add_bin_op()` method wraps a binary operator.  Its parameters are:

```
  def add_bin_op(
    self,
    op,
    returns,
    params,
```

The `op` parameter is the name of the operator, and must be a valid C++ binary operator such as `+`, `-`, `*`, `/`, `%`; or `==`, `!=`, `<`, and so on.

The `returns` parameter is the C++ type name for the return value of the operator.  The `params` is the list of parameters; it must be of length 2.  As such, the binary operator doesn't implicitly involve the type that `add_bin_op()` is called on.

The result of `add_bin_op()` supports `add_comment(comment)` and `add_test(kl, out)`.

Binary operators in C++ are wrapped to the same binary operator in KL.  For example:

```
ty.add_bin_op('==', 'bool', [Param('lhs', 'MyType const &'), Param('rhs', 'MyType const &')])
```

is mapped to:

```
Boolean +(MyType_CxxConstRef, MyType_CxxConstRef);
```

## `add_ass_op()`

The `add_ass_op()` method adds an assignment operator.  Its parameters are:

```
  def add_ass_op(
    self,
    op,
    params,
    ):
```

The `op` parameter must be an assignment operator, either plain or compound, such as `=`, `+=`, etc. The `params` parameter must have length one.

The result of `add_ass_op()` supports `add_comment(comment)` and `add_test(kl, out)`.

C++ assignment operators are mapped to KL assignment operators directly.  For example:

```
ty.add_ass_op('+=', ['int'])
```

becomes:

```
MyType.+=(SInt32 val);
```


## `add_cast()`

The `add_cast()` method adds a cast from the type to a different type.  Its parameters are:

```      
  def add_cast(
    self,
    dst,
    this_access=ThisAccess.const,
    ):
```

The `dst` parameter is the C++ type for the destination type.  `this_access` can be either `ThisAccess.const` or `ThisAccess.mutable`.

The result of `add_cast()` supports `add_comment(comment)` and `add_test(kl, out)`.

Note that casts in C++ are represented as constructors in KL, as shown in the example:

```
ty.add_cast('int');
```

which produces:

```
SInt32(MyType);
```

## `add_get_ind_op()` and `add_set_ind_op()`

The `add_get_ind_op()` and `add_set_ind_op()` methods wrap the use of C++ `operator[]`, the former for getting values and the latter for setting values.

The parameters are:

```
  def add_get_ind_op(
    self,
    value_cpp_type_name,
    this_access = ThisAccess.const
    ):
  def add_set_ind_op(
    self,
    value_cpp_type_name,
    this_access = ThisAccess.mutable
    ):
```

The `value_cpp_type_name` is the type name of the value that is get or set; for `add_get_ind_op()` it is the return value, and for `add_set_ind_op()` it is the second parameter value.  The first parameter value in each case is of type `Index` in KL and `size_t` in C++ (at some point we will allow this to be overridden).  `this_access` controls the mutability of the type for each case.

The index operations are mapped to the methods `cxxGetAtIndex` and `cxxSetAtIndex`, respectively. The result of `add_get_ind_op()` or `add_set_ind_op()` supports `add_comment(comment)` and `add_test(kl, out)`.

For example:

```
ty.add_get_ind_op('float')
ty.add_set_ind_op('float')
```

produces:

```
Float32 MyType.cxxGetAtIndex?(Index index);
MyType.cxxSetAtIndex!(Index index, Float32 value);
```

## `add_deref()`

The `add_deref()` method maps the C++ `operator *()` that acts as a deference operation.  This is commonly used in iterators.  The parameters are:

```
  def add_deref(
    self,
    returns,
    this_access = ThisAccess.const,
    kl_method_name = 'cxxDeref',
    ):
```

All of the parameters are as for other methods above.  The result of `add_deref()` supports `add_comment(comment)` and `add_test(kl, out)`.

Example:

```
ty.add_deref('int');
```

Produces:

```
SInt32 MyType.cxxDeref?();
```

## `add_kl()`

The `add_kl()` method allows you to append a Jinja2 template of KL code to be included in the generated KL for the extension.  Its parameters are:

```
  def add_kl(
    self,
    code,
    **kwargs
    ):
```

The `code` parameter is the Jinja2 template to be used.  It will be passed a template variable `type_name` which is the KL type name for the type.  Additional values can be passed as additional arguments in Python through the `kwargs` parameter; these will be passed by name to the template.

## `add_comment()`

The `add_comment()` method adds a comment that will appear, verbatim, above the type declaration in KL.  The comment must include KL commenting delimiters.  This is used by `kludge discover` to import C++ comments into KL comments.

## `set_default_visibility()`

Set the default visibility to one of `Visibility.public`, `Visibility.protected` or `Visibility.private` for when it is omitted for member declarations.

Next: [Methods Affecting Compilation](adl-comp-methods.md)
