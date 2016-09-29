# Unit Tests

Kludge makes it easy to add unit tests using the API description language.  The `kludge generate` step generates three additional files to support unit tests:

- `ExtensionName.test.kl` is a KL program that contains the unit tests.  It requires the generated extension and runs the tests, producing test output on standard output.

- `ExtensionName.test.out` contains the expected output from running `ExtensionName.test.kl`

- `ExtensionName.test.py` is a Python script that runs `ExtensionName.test.kl` and ensures that its output matches `ExtensionName.test.out`.  If it does not, it shows diffs of the output that will help isolate why the test is failing.

Unit tests are added via the `add_test(kl, out)` method which can be called on methods, types, functions or the extension itself.  The `kl` parameter is the KL code that is the test itself, and the `out` parameter is the output.  The recommended use is with Python triple-quote strings, for example:

```
my_type.add_test("""
MyType value(14);
report(value.method());
""", """
42
""")
```

To see an example of unit tests in Kludge, create the file `Fact.hpp`:

```
#pragma once

inline int Fact( int n ) {
  if ( n > 1 )
    return n * Fact( n - 1 );
  else
    return 1;
}
```

Run it through `kludge discover`:

```
path/to/kludge discover Fact Fact.hpp
```

Edit the resulting `Fact.kludge.py` file and add the following to the end:

```
ext.add_test("""
for (SInt32 i = 0; i < 6; ++i)
  report("Fact(" + i + ") = " + Fact(i));
""", """
Fact(0) = 1
Fact(1) = 1
Fact(2) = 2
Fact(3) = 6
Fact(4) = 24
Fact(5) = 120
""")
```

Generate and compile the extension:

```
path/to/kludge generate Fact Fact.kludge.py
scons -f Fact.SConstruct
```

Finally, run the unit tests:

```
python Fact.test.py
```

You should see `Fact extension tests passed!`.  Try editing the unit test output (or the test) in `Fact.kludge.py`, re-running `kludge generate` and then `python Fact.test.py`; the resulting output should show you where the test failed.
