# Namespaces in Kludge

C++ has support for nested namespaces; however, KL does not (yet) support namespaces.  As such, Kludge maps C++ namespaces to KL nested names using a `Prefixed_With_Underscores_` syntax.

The root `ext` object that is provided to the API description language also represents the root namespace.  A nested namespace can be added with the `ext.add_namespace(method)`.  Its parameters are:

```
  def add_namespace(self, cpp_name, kl_name=None):
```

The `cpp_name` is the name of the namespace in C++, and is required.  `kl_name` is the name that should be used for prefixing in KL, and if not provided defaults to the `cpp_name`.

The resulting namespace object can in turn have types added to see as described in [How Kludge Wraps Types](wrapping-types.md), have functions added to it [How Kludge Wraps Functions](functions.md), or even have sub-namespaces created below it.

This is illustrated with an example.  The following API description:

```
ns = ext.add_namespace('MyLib')
ty = ns.add_owned_type('SomeType')
ty.add_const_method('Foo', 'int')
sns = ns.add_namespace('ChildNS')
sns.add_alias('IntType', 'int')
```

would result in the KL API:

```
struct MyLib_SomeType {...};
SInt32 MyLib_SomeType.Foo?();
alias SInt32 MyLib_ChildNS_IntType;
```

Note that wrapping a type (for example, using `.add_owned_type()`) also creates a child namespace.  This is important functionality that allows, for instance, enums and type aliases to be scoped under classes or structs:

```
ty = ext.add_type("SomeType")
ty.add_enum("SomeEnum", ['ValueOne', 'ValueTwo'])
```

produces:

```
struct SomeType {...};
alias SInt32 SomeType_SomeEnum;
const SomeType_ValueOne = 0;
const SomeType_ValueTwo = 1;
```

## C++ type lookups

It is important to note that C++ types are looked up in the namespace where they are referenced.  This works exactly as you would expect in C++.

