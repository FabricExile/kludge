# An Example with Types

The next tutorial example wraps an API that has C++ types.  Begin by creating the files `Counter.hpp`:

```
#pragma once

class Counter
{
public:

  Counter() : value(0) {}

  int getValue() const { return value; }

  void increment() { value++; }

  void add( int amount ) { value += amount; }

  void reset() { value = 0; }

private:

  int value;
};
```

Since the class is entirely self-container, we do not need a corresponding `Counter.cpp` and do not need to compile a shared library for the class.

Use Kludge's discover tool to build an API description of the header:

```
path/to/kludge discover Counter Counter.hpp
```

Take a look at the resulting `Counter.decls.kludge.py`.  The line

```
ext_Counter = ext.add_owned_type('Counter')
```

This line tells Kludge that there is a type named `Counter` in C++ that should be available in KL (with the same name).  The term `owned` refers to the way in which the type is mapped into KL; there are different ways of doing this and they are covered later in [Type Wrapping Semantics](types.md).

Now examine `Counter.defns.kludge.py`.  The non-comment lines are:

```
ext_Counter.add_member('value', 'int', visibility=Visibility.private)
ext_Counter.add_ctor([])
ext_Counter.add_method('getValue', 'int', [], this_access=ThisAccess.const)
ext_Counter.add_method('increment', 'void', [], this_access=ThisAccess.mutable)
ext_Counter.add_method('add', 'void', [Param('amount', 'int')], this_access=ThisAccess.mutable)
ext_Counter.add_method('reset', 'void', [], this_access=ThisAccess.mutable)
```

These lines are fairly self explanitory, but the details are:

- The `add_member` line adds a member to the type.  Since the member is private it is not strictly necessary to provide this line, but Kludge discover does anyway for completeness.  (Note that if the type is declared using `add_in_place_type` as covered in [Type Wrapping Semantics](types.md) then the members must be provided even if they aren't public) 

- The `add_ctor` line adds a constructor for the type.  The constructor takes no parameters, as indiciated by the empty array.

- The `add_method` lines add methods to the type.  In each case the parameters are the name of the method, the return type, and the list of parameters, and finally the `ThisAccess` which specifies if the function is `const`, `static` or "mutable" (neither `static` nor `const`).

Now, use `kludge generate` to generate the extension:

```
path/to/kludge generate Counter Counter.kludge.py
```

Feel free to take a look at `Counter.kl` and `Counter.cpp`; they are more complicated than before but still understandable.  For now, we will just go ahead use the extension.  First, compile it:

```
scons -f Counter.SConstruct
```

Then create `test.kl`:

```
require Counter;
operator entry() {
  Counter c;
  report("initial: " + c.getValue());
  c.increment();
  report("after increment: " + c.getValue());
  c.reset();
  report("after reset: " + c.getValue());
  c.add(42);
  report("after add(42): " + c.getValue());
}
```

and run it:

```
FABRIC_EXTS_PATH=. kl test.kl
```

You should see the following output:

```
initial: 0
after increment: 1
after reset: 0
after add(42): 42
```

[Next: An Extension with Types](tutorial-types.md)
