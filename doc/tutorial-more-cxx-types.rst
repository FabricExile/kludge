.. _KludgeTutorialMoreCxxTypes:

Tutorial: More About Using C++ Types
========================================

In the last tutorial we had to explicitly convert a KL array of integers into an STL vector in order to call a C++ function to reverse the elements of the vector.

An obvious question is, why doesn't Kludge just automatically convert the vector?  The answer lies in a key design aspect of Kludge: **Kludge will try to make the extension as easy to use as possible, but not at the cost of significant performance loss**.

In this case, if we were to implicitly convert KL vectors into STL vectors, there would be a hidden performance cost that users need to be aware of.  For a large vector (with hundreds of million of elements) the cost of converting the vector back and forth is significant and should be avoided.

So how does one avoid this conversion?  The answer is that Kludge allows you to use C++ types directly without ever using KL types for cases where this performance really matters.  This is illustrated with the following example that uses the ``STLUser`` extension we built in the last tutorial:

.. code-block:: kl

  require STLUser;
  operator entry() {
    CxxSInt32StdVector a;
    for (SInt32 i = 0; i < 10; ++i)
      a.push_back(i);
    report("a = " + a);
    report("ReverseVector(a) = " + ReverseVector(a));
  }

Running this gives the output:

.. code-block:: none

  a = CxxSInt32StdVector:[0,1,2,3,4,5,6,7,8,9]
  ReverseVector(a) = CxxSInt32StdVector:[9,8,7,6,5,4,3,2,1,0]

The result is the same, but we just created the STL vector directly rather than converting one from KL.  Notice that the STL vector was created using the ``push_back`` method rather than the KL equivalent ``push`` method; this is because this is how the method is named in C++.

Using C++ Pointers and References
------------------------------------------

Since Kludge prioritizes performance over ease of use, Kludge needs to provide a way to cooperate with C++'s heavy use of pointers and references.  In C++, pointers and references are often used as a mechanism to avoid making copies of data, and Kludge provides a reflection mechanism of C++ pointers and references into KL.  We will now see this in action.

Let's begin with an example header file, :file:`RefEx.hpp`:

.. code-block:: c++
  :caption: RefEx.hpp

  #pragma once

  #include <string>
  #include <vector>

  inline std::string const &LongestString( std::vector<std::string> const &vs )
  {
    std::vector<std::string>::const_iterator longestIT = vs.begin();
    for ( std::vector<std::string>::const_iterator it = longestIT + 1; it != vs.end(); ++it )
      if ( it->size() > longestIT->size() )
        longestIT = it;
    return *longestIT;
  }

Build as before:

.. code-block:: console

  $ kludge discover RefEx RefEx.hpp
  $ kludge generate RefEx RefEx.kludge.py
  $ scons -f RefEx.SConstruct

Run it using the following :file:`test.kl`:

.. code-block:: kl

  require RefEx;
  operator entry() {
    CxxStdStringStdVector vs;
    vs.push_back(Make_CxxStdString("one"));
    vs.push_back(Make_CxxStdString("two"));
    vs.push_back(Make_CxxStdString("three"));
    vs.push_back(Make_CxxStdString("four"));
    vs.push_back(Make_CxxStdString("five"));
    CxxStdStringConstRef longest = LongestString(vs);
    report("longest = " + longest);
    report("longest.size() = " + longest.size());
  }

You should see the output

.. code-block:: none

  longest = three
  longest.size() = 5

as expected.  The key thing to notice here, however, is that we didn't construct a new KL string with the result; instead, we have a value of type ``CxxStdStringConstRef``.  This KL type corresponds to the C++ type ``std::string const &`` and it allows us to avoid copying an actual string.  In this case it wouldn't matter much, but in the case where the string had millions of characters -- or it was a different heavyweight type -- it can make a big difference.

Similar to ``Cxx...ConstRef``, Kludge also supports ``Cxx...Ref``, ``Cxx...ConstPtr`` and ``Cxx...Ptr``.  One of the properties that these types have are that they automatically can use the methods of the type they refer or point to (as seen above), which allows you to avoid converting it to an actual instance of the type.  And, just like C++ pointers and references, you must be very careful when using them: it's easy to create code where the pointer or reference points to a value that has been destroyed.

Fortunately, for many use cases you don't have to worry about them if it's not important.  This is because there is (usually) an automatic conversion between pointers and references and the underlying type.  So, for example, this code would work as well:

.. code-block:: kl

  require RefEx;
  operator entry() {
    CxxStdStringStdVector vs;
    vs.push_back(Make_CxxStdString("one"));
    vs.push_back(Make_CxxStdString("two"));
    vs.push_back(Make_CxxStdString("three"));
    vs.push_back(Make_CxxStdString("four"));
    vs.push_back(Make_CxxStdString("five"));
    String longest = LongestString(vs);
    report("longest = " + longest);
    report("longest.length() = " + longest.length());
  }

More about C++ pointers and references can be found in the section :ref:`KludgePtrsRefs`.
