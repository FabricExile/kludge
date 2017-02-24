# Wrapping Types

There are multiple ways of wrapping types in Kludge; which way should be used depends on the semantics of the C++ API that is being wrapped.  Unfortunately, it is difficult-to-impossible for Kludge to make an intelligent guess as to which way should be used, and as such it is left up to the user to edit the output of the `kludge discover` command to make changes to way that types are wrapped.

The way in which a type is wrapped is dictated by the method used to create the type in the API description language.  So far we have only seen `ext.add_owned_type(...)`; below, we enumerate all of the ways types can be wrapped.

## `ext.add_owned_type()`

The *owned* mechanism of wrapping types is the default for Kludge.  In this context, "owned" is a bit of a misnomer; what it means is that Kludge allocates a copy of the C++ value (using the C++ `new` operator) which it then deletes when the value goes out of scope in KL.  This is a safe way of representing the type in KL that works for most types but gives up a bit of performance since the value is stored indirectly, on the program heap.

The actual parameters of `.add_owned_type()` are

```
  def add_owned_type(
    self,
    cpp_type_name,
    kl_type_name=None,
    extends=None,
    forbid_copy=False,
    is_abstract=False,
    ):
```

The only required parameter is `cpp_type_name`, which is the C++ type that is being wrapped.  By default the type will have the same name in KL, but this can be overridden with the `kl_type_name` parameter.

The `extends` parameter indicates C++ inheritance; in practice, it means that this type will have all the (public) methods of the type that it extends.

The `forbid_copy` parameter prevents users from copying values of this type; this is mostly meant to be used when copying has been forbidden in C++.  The `is_abstract` parameter indicates that the type is abstract and can't be instantiated at all; however, it can be used in the `extends` clause of another type.  A value of this type can also be used through a pointer or reference to it.

The result of the `ext.add_owned_type()` call is a record object which can be used to add constructors, methods and so on to the type (see [Wrapping Methods and Method-Like Type Additions](adl-methods.md)).

## `ext.add_in_place_type()`

The *in-place* mechanism for wrapping types makes the KL memory layout of the type exactly match that in C++.  This means that the type is stored directly, which can make a positive difference for performance under certain circumstances.  However, it must be the case that all of the members of type are correctly specified in Kludge, in the right order, and they must all, too, be wrapped in-place.  **Note that Kludge currently does not do anything to ensure that these conditions are met; failing to meet them will cause unpredictable results with your extension, usually crashes.**

All of the simple numeric types in C++ such as `int` and `float` are automatically wrapped in-place.  Compound types can also be wrapped in-place; good examples of types that can be wrapped in place are fixed-size vectors, quaternions, fixed-size matrices, and any other class or struct whose members are (recursively) composed of simple C++ types.  Note however that for certain cases it makes sense to use the `.add_mirror()` method instead (see below).

The parameters of the `ext.add_in_place_type()` method are identical in name and function to those of `ext.add_owned_type()`.

The result of the `ext.add_owned_type()` call is a record object which can be used to add constructors, methods and so on to the type (see [Wrapping Methods and Method-Like Type Additions](adl-methods.md)).

## `ext.add_opaque_type()`

The *opaque* mechanism for wrapping types is used when then API manages an API type as an opaque pointer.  This mechanism is often used in pure C APIs; an example of such an API is given in the following sample code:

```
class MyOpaque;

MyOpaque *MyOpaque_New( int x );
int MyOpaque_GetX( MyOpaque const *_r );
void MyOpaque_SetX( MyOpaque *_r, int x );
void MyOpaque_Delete( MyOpaque *_r );
```

The parameters for `.add_opaque_type()` are:

```
  def add_opaque_type(
    self,
    cpp_type_name,
    kl_type_name=None,
    extends=None,
    ):
```

The `extends` parameter acts a little bit differently than for other types.  It is not required that the C++ type actually inherits from the type given by `extends`; instead, Kludge assumes that it is safe to `reinterpret_cast` to the derived type.  This is because many C APIs use opaque pointers exactly in this manner.

The result of the `ext.add_opaque_type()` call is a record object that can be used to add tests to the type.  Note, however, that it is not currently possible to add methods or members to opaque types through the Kludge specification language; currently, the only way to use opaque types is through functions.  However, you can provide boilerplate code that wraps these functions as methods.

## `ext.add_wrapped_type()`

The *wrapped* mechanism for wrapping types is used to hold a value that is contained by a C++ template; the most common use case of this is when the value is owned by some sort of shared pointer template, but it is not limited to only this case; it will generally work with any template which exposes the two C++ operators `operator->()`, to access the value the template owns, and `bool operator !`, to assess if the template points to a NULL value.

The parameters for `.add_wrapped_type()` are:

```
  def add_wrapped_type(
    self,
    cpp_wrapper_name,
    cpp_type_name,
    kl_type_name=None,
    extends=None,
    forbid_copy=False,
    is_abstract=False,
    ):
```

The only additional parameters is `cpp_wrapped_name`, which is the name of the C++ template that wraps the owned value.  For example, if the type that is being wrapped is called `DataBlob` and it is owned through the `SharedPtr` template, then the type would be wrapped with `ext.add_wrapped_type('SharedPtr', 'DataBlob')`.  Internally, Kludge will own a copy of a value of type `SharedPtr<DataBlob>`, thus respecting the shared pointer semantics.

Additional notes about types wrapped with `ext.add_wrapped_type()`:

- References and pointers for the type, for example `CxxDataBlockConstPtr` using the above syntax, does not point to the wrapped value but rather the unwrapped value (i.e. the result of `operator->()`).  It is still possible to get pointers and references to wrapped values; their type is prefixed with `Wrapped`; for example, `CxxWrappedDataBlockConstPtr`.

- Kludge does track the underlying type that is wrapped via the template, but it will not generally be needed; it is prefixed with `CxxRaw`; for example, `CxxRawDataBlob`.

The result of the `ext.add_owned_type()` call is a record object which can be used to add constructors, methods and so on to the type (see [Wrapping Methods and Method-Like Type Additions](adl-methods.md)).

## `ext.add_mirror()`

A mirror is a special kind of type mapping that is used when a C++ type already has an identical representation in KL and we want to use the KL representation when working in KL.  This is commonly used for math types such as the KL Math extensions `Vec3` type.  None of the C++ methods are made available in KL, and instead the user will use the KL functions to work with the type in KL.

The parameters for `ext.add_mirror()` are:

```
  def add_mirror(
    self,
    cpp_local_name,
    existing_kl_global_name,
    kl_ext_name=None,
    ):
```

The `cpp_local_name` and `existing_kl_global_name` are the C++ and KL names for the type, respectively; they can be identical.  If present the `kl_ext_name` is the name of the extension that needs to be required for the KL type (such as `Math`).  So, for example, if a C++ library provides a three 32-bit float element vector in the same order as KL, called `V3f`, the type mirror would be specified with `ext.add_mirror('V3f', 'Vec3', 'Math')`.

Note that pointers and references to the type will still be available, but they will use the C++ name (since pointers and references are a C++ concept).  So, for example, the C++ function:

```
V3f const *GetV3fPtr();
```

would appear in KL as:

```
CxxV3fConstPtr GetV3fPtr();
```

The result will need to be dereferenced for any of its methods to be used, for example:

```
Vec3 vec3 = GetV3fPtr().cxx_deref();
```

## `ext.add_enum()`

The `ext.add_enum()` method maps a C++ enum to a KL type alias and a set of constants (since KL doesn't yet support enums).  The syntax is:

```
  def add_enum(
    self,
    cpp_local_name,
    values,
    kl_local_name = None,
    are_values_namespaced = False,
    ):
```

`cpp_local_name` is the name of the enum in C++, and values is the array of values of the enum.  The values can either be a (string, integer) tuple, which gives the integer value to the named enum value, or simply a string, in which case the next integer value is used (following the same rules as C++; by default, the first value is 0).  `kl_local_name` is the (optional) name of the enum in KL; if omitted it will be the C++ name.

The `are_values_namespaced` flag indicates whether the values of the enum are in a nested namespace or not (see [Wrapping Namespaces](adl-namespaces.md) for more information on namespace handling in Kludge).  For example, the enum:

```
ext.add_enum('Fruit', ['Apple', 'Orange'])
```

would produce the KL code:

```
alias SInt32 Fruit;
const Fruit Apple = 0;
const Fruit Orange = 1;
```

whereas:

```
ext.add_enum('Fruit', ['Apple', 'Orange'], are_values_namespaced=True)
```

would produce:

```
alias SInt32 Fruit;
const Fruit Fruit_Apple = 0;
const Fruit Fruit_Orange = 1;
```

You can choose to wrap an enum either way, but, generally speaking, you should use `are_values_namespaced=False` for "classic" C++ enums and `are_values_namespace=True` for C++11 `enum class` declarations.

## `ext.add_alias()`

The `ext.add_alias()` method creates a simple KL type alias.  It takes the parameters:

```
  def add_alias(self, new_cpp_type_name, old_cpp_type_name):
```

It can general be used to represent C++ `typedef` and `using <type name> =` declarations.

## `ext.add_ignored_type()`

The `ext.add_ignored_type()` method can be used to define a type which should be ignored during the generation. If the specified C++ type is added later through any of the `ext.add_type` methods, it will simply be ignored.

```
  def add_ignored_type(self, cpp_type_name):
```

This is useful if you want to rely on the discover step to generate the kludge files but also need to ensure to skip certain types since they might cause issues.

Next: [Wrapping Namespaces](adl-namespaces.md)
