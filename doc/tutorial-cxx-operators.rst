.. _KludgeTutorialCxxOperators:

Tutorial: C++ Operators
===============================

The next tutorial example shows how C++ operators are wrapped in Kludge.  Begin with the file :file:`MyInt.hpp`:

.. code-block:: c++
  :caption: MyInt.hpp

  #pragma once

  class MyInt
  {
  public:

    MyInt() : value(0) {}
    MyInt(int v) : value(v) {}

    MyInt operator +(MyInt const &rhs) const
      { return MyInt(value + rhs.value); }

    MyInt &operator +=(MyInt const &rhs)
    {
      value += rhs.value;
      return *this;
    }

    MyInt &operator ++()
    {
      ++value;
      return *this;
    }

    operator int() const
      { return value; }


  private:

    int value;
  };

Use Kludge's discover tool to build an API description of the header, then generate and compile the extension:

.. code-block:: console

  $ kludge discover MyInt MyInt.hpp
  $ kludge generate MyInt MyInt.kludge.py
  $ scons -f MyInt.SConstruct

The type exposes a bunch of C++ operators.  How are they exposed in KL?  This is best illustrated with :file:`test.kl`:

.. code-block:: kl
  :caption: test.kl for MyInt extension

  require MyInt;
  operator entry() {
    MyInt a(7), b(5);
    report("initially:");
    report("a = " + SInt32(a));
    report("b = " + SInt32(b));
    report("a + b = " + SInt32(a+b));
    a.cxx_inc();
    report("after a.cxx_inc():");
    report("a = " + SInt32(a));
    report("b = " + SInt32(b));
    report("a + b = " + SInt32(a+b));
    a += b;
    report("after a += b:");
    report("a = " + SInt32(a));
    report("b = " + SInt32(b));
    report("a + b = " + SInt32(a+b));
  }

Running this as

.. code-block:: console

  $ FABRIC_EXTS_PATH=. kl test.kl

we get the output

.. code-block:: none

  initially:
  a = 7
  b = 5
  a + b = 12
  after a.cxx_inc():
  a = 8
  b = 5
  a + b = 13
  after a += b:
  a = 13
  b = 5
  a + b = 18

So how exactly are the operators mapped to KL?

- The line ``MyInt a(7), b(5);`` uses the C++ constructor that takes an ``int`` to create instances of the C++ type in KL

- The line ``report("a = " + SInt32(a));`` uses the ``operator int`` of ``MyInt`` to allow conversion of ``MyInt`` to a KL SInt32 (which is equivalent to a C++ int)

- The line ``report("a + b = " + SInt32(a+b));`` uses the ``operator +`` of ``MyInt`` to add two values of the type

- The line ``a.cxx_inc();`` calls the ``operator ++`` of ``MyInt``.  We need this special syntax because there's currently no way to overload ``++`` (and ``--``) in KL

- The line ``a += b;`` calls the ``operator +=`` of ``MyInt``.

As you can see, in all cases but the increment operator the mapping from C++ to KL is direct: we use exactly the same syntax in KL as we do in C++.  In the case of increment, we use the special `cxx_inc` method to perform the increment.  This is a pattern you will see often in Kludge: when there is no direct KL analog for something in C++ it will be available through a method or type that includes `cxx` or `Cxx` in the name.  More information on how operators are wrapped can be found in :ref:`KludgeADLMethods`.
