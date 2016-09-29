# Tutorial: More About Using C++ Types

In the last tutorial we had to explicitly convery a KL array of integers into an STL vector in order to call a C++ function to reverse the elements of the vector.

An obvious question is, why doesn't Kludge just automatically convert the vector?  The answer lies in a key design aspect of Kludge: **Kludge will try to make the extension as easy to use as possible, but not at the cost of significant performance loss**.

In this case, if we were to implicitly convert KL vectors into STL vectors, there would be a hidden performance cost that users need to be aware of.  For a large vector (with hundreds of million of elements) the cost of converting the vector back and forth is significant and should be avoided.

So how does one avoid this conversion?  The answer is that Kludge allows you to use C++ types directly without ever using KL types for cases where this performance really matters.  This is illustrated with the following example that uses the `STLUser` extension we built in the last tutorial:

```
require STLUser;
operator entry() {
  SInt32_StdVector a;
  for (SInt32 i = 0; i < 10; ++i)
    a.push_back(i);
  report("a = " + a);
  report("ReverseVector(a) = " + ReverseVector(a));
}
```

Running this gives the output:

```
a = SInt32_StdVector:[0,1,2,3,4,5,6,7,8,9]
ReverseVector(a) = SInt32_StdVector:[9,8,7,6,5,4,3,2,1,0]
```

The result is the same, but we just created the STL vector directly rather than converting one from KL.  Notice that the STL vector was created using the `push_back` method rather than the KL equivalent `push` method; this is because this is how the method is named in C++.

## Using C++ Pointers and References

Since Kludge prioritizes performance over ease of use, Kludge needs to provide a way to cooperate with C++'s heavy use of pointers and references.  In C++, pointers and references are often used as a mechanism to avoid making copies of data, and Kludge provides a reflection mechanism of C++ pointers and references into KL.  We will now see this in action.

Let's begin with an example header file, 'RefEx.hpp':

```
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
```

Build as before:

```
path/to/kludge discover RefEx RefEx.hpp
path/to/kludge generate RefEx RefEx.kludge.py
scons -f RefEx.SConstruct
```

Run it using the following `test.kl`:

```
require RefEx;
operator entry() {
  StdString_StdVector vs;
  vs.push_back(Make_StdString("one"));
  vs.push_back(Make_StdString("two"));
  vs.push_back(Make_StdString("three"));
  vs.push_back(Make_StdString("four"));
  vs.push_back(Make_StdString("five"));
  String longest = LongestString(vs);
  report("longest = " + longest);
  report("longest.size() = " + longest.size());
}
```

You should see the output

```
three
5
```

as expected.  The key thing to notice here, however, is that we didn't construct a new KL string with the result; instead, we have a value of type `StdString_CxxConstRef`.  This KL type corresponds to the C++ type `std::string const &` and it allows us to avoid copying an actual string.  In this case it wouldn't matter much, but in the case where the string had millions of characters -- or it was a different heavyweight type -- it can make a big difference.

Similar to `_CxxConstRef`, Kludge also supports `_CxxRef`, `_CxxConstPtr` and `_CxxPtr`.  One of the properties that these types have are that they automatically can use the methods of the type they refer or point to (as seen above), which allows you to avoid converting it to an actual instance of the type.  And, just like C++ pointers and references, you must be very careful when using them: it's easy to create code where the pointer or reference is to a value that has been destroyed.

Fortunately, for many use cases you don't have to worry about them if it's not important.  This is because there is (usually) an automatic conversion between pointers and references and the underlying type.  So, for example, this code would work as well:

```
require RefEx;
operator entry() {
  StdString_StdVector vs;
  vs.push_back(Make_StdString("one"));
  vs.push_back(Make_StdString("two"));
  vs.push_back(Make_StdString("three"));
  vs.push_back(Make_StdString("four"));
  vs.push_back(Make_StdString("five"));
  String longest = LongestString(vs);
  report("longest = " + longest);
  report("longest.length() = " + longest.length());
}
```

Pointers and references will be covered in more detail in the reference section of the documentation.
