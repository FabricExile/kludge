# Pointers and References

As discussed previously, Kludge will automatically wrap pointer and reference types that are used by C++ for parameter and return values.  For a given type `MyType` these take the form `CxxMyTypeConstPtr`, `CxxMyTypeConstRef`, `CxxMyTypePtr` and `CxxMyTypeRef`.

The basic features that all of these types have are:

- They do not "own" what they point to but rather have an unowned pointer to it.  As such, they are generally faster to use than copying values around; however, they can also be dangerous.

- They "reflect" the methods of the underlying type.  For instance, if `MyType` has a method `MyType.foo(SInt32)`, so do `CxxMyTypeConstPtr`, `CxxMyTypeConstRef`, `CxxMyTypePtr` and `CxxMyTypeRef`.  Note however that only `CxxMyTypePtr` and `CxxMyTypeRef` will reflect the mutable (non-const in C++, `!` in KL) methods for the type.  Note also that other method-like things for types, such as constructors and casts, are not reflected in pointer and reference types.

- Casting from `MyType` to each pointer and reference type is *usually* implicit, but sometimes requires an explicit call to eg. `Make_CxxMyTypeConstPtr()`.  This is particularly required for casts from simple, built-in types like `SInt32` and `Float32` and is due to the implicit casting rules in KL.

- Creating a value of a pointer or reference type will initially point to nothing, i.e. will be null.  Trying to use this value (eg. by calling a method on it) will throw an exception in KL.  Use `CxxMyTypeConstPtr.cxx_isValid()`, or just the cast

Furthermore, each of these types expose a few extra methods to let you work with them, as described below.

## `_CxxConstPtr` Methods

- `Boolean CxxMyTypeConstPtr.cxx_isValid()` checks that it is not null.  We also provide the cast to `Boolean` that achieves the same thing.

- `CxxMyTypeConstRef CxxMyTypeConstPtr.cxx_getAt(Index)` returns a `CxxMyTypeConstRef` to the element at a given index in the same way as the C++ indexing operator.  No bounds checking is performed (nor could be performed since C++ does not bounds check on raw pointers).

- `CxxMyTypeConstRef CxxMyTypeConstPtr.cxx_deref()` dereferences the pointer; equivalent to `CxxMyTypeConstPtr.cxx_getAt(0)`

## `_CxxPtr` Methods

`_CxxPtr` supports all the methods of `_CxxConstPtr` except that they return a `_CxxRef` rather than a `_CxxConstRef` where appropriate.  They additional support the methods:

- `CxxMyTypePtr.cxx_setAt(Index, MyType)` sets the value at the given index.  Equivalent to `MyType_Cxxptr.cxx_getAt(Index).cxx_set(MyType)`.

## `_CxxConstRef` Methods

- `MyType CxxMyTypeConstRef.cxx_get()` returns a copy of the value that's referenced.  We also provide `MyType(CxxMyTypeConstRef)` as an implicit call to `MyType CxxMyTypeConstRef.cxx_get()`.

## `Cxx...Ref` Methods

`Cxx...Ref` supports all the methods of `Cxx...ConstRef`, and additionally supports the methods:

- `CxxMyTypeRef.cxx_set(MyType)` sets the value of the reference value, i.e. performs a C++ assign of the value.

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
