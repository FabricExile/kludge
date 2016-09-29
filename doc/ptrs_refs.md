# Pointers and References

As discussed previously, Kludge will automatically wrap pointer and reference types that are used by C++ for parameter and return values.  For a give type `MyType` these take the form `MyType_CxxConstPtr`, `MyType_CxxConstRef`, `MyType_CxxPtr` and `MyType_CxxRef`.

The basic features that all of these types have are:

- They do not "own" what they point to but rather have an unowned pointer to it.  As such, they are generally faster to use than copying values around; however, they can also be dangerous.

- They "reflect" the methods of the underlying type.  For instance, if `MyType` has a method `MyType.foo(SInt32)`, so do `MyType_CxxConstPtr`, `MyType_CxxConstRef`, `MyType_CxxPtr` and `MyType_CxxRef`.  Note however that only `MyType_CxxPtr` and `MyType_CxxRef` will reflect the mutable (non-const in C++, `!` in KL) methods for the type.  Note also that other method-like things for types, such as constructors and casts, are not reflected in pointer and reference types.

- Casting from `MyType` to each pointer and reference type is *usually* implicit, but sometimes requires an explicit call to eg. `Make_MyType_CxxConstPtr()`.  This is particularly required for casts from simple, built-in types like `SInt32` and `Float32` and is due to the implicit casting rules in KL.

- Creating a value of a pointer or reference type will initially point to nothing, ie. will be null.  Trying to use this value (eg. by calling a method on it) will throw an exception in KL.  Use `MyType_CxxConstPtr.cxxIsValid()`, or just the cast

Furthermore, each of these types expose a few extra methods to let you work with them, as described below.

## `_CxxConstPtr` Methods

- `Boolean MyType_CxxConstPtr.cxxIsValid()` checks that it is not null.  We also provide the cast to `Boolean` that achieves the same thing.

- `MyType_CxxConstRef MyType_CxxConstPtr.cxxGetAt(Index)` returns a `MyType_CxxConstRef` to the element at a given index in the same way as the C++ indexing operator.  No bounds checking is performed (nor could be performed since C++ does not bounds check on raw pointers).

- `MyType_CxxConstRef MyType_CxxConstPtr.cxxDeref()` dereferences the pointer; equivalent to `MyType_CxxConstPtr.cxxGetAt(0)`

## `_CxxPtr` Methods

`_CxxPtr` supports all the methods of `_CxxConstPtr` except that they return a `_CxxRef` rather than a `_CxxConstRef` where appropriate.  They additional support the methods:

- `MyType_CxxPtr.cxxSetAt(Index, MyType)` sets the value at the given index.  Equivalent to `MyType_Cxxptr.cxxGetAt(Index).cxxSet(MyType)`.

## `_CxxConstRef` Methods

- `MyType MyType_CxxConstRef.cxxGet()` returns a copy of the value that's referenced.  We also provide `MyType(MyType_CxxConstRef)` as an implicit call to `MyType MyType_CxxConstRef.cxxGet()`.

## `_CxxRef` Methods

`_CxxRef` supports all the methods of `_CxxConstRef`, and additionally supports the methods:

- `MyType_CxxRef.cxxSet(MyType)` sets the value of the reference value, ie. peforms a C++ assign of the value.

## The `CxxCharConstPtr` Type

Because of complications with the `char` type in C++ we provide `CxxCharConstPtr`, `CxxCharPtr`, `CxxCharConstRef` and `CxxCharRef` and the pointer and reference types to `char`.  They have the same properties as other pointer and reference types with the additional features that the cast from `CxxCharConstPtr` to a KL `String` assumes that the `CxxCharConstPtr` points to a C string.  This is usually the case, but beware that if it doesn't point to a valid C string then your KL program may crash when performing this conversion!  The reason for this conversion behaviour is so that a function such as:

```
ext.add_func('ReturnHelloWorld', 'char const *')
```

can be used in KL as:

```
report(ReturnHelloWorld());
```

and work as expected.

Next: [Unit Tests](unit-tests.md)
