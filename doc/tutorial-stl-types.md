# Tutorial: STL Types and Instantiating Templates

Kludge provides some basic mechanisms for automatic wrapping of STL types including `std::string` and `std::vector`.  This is illustrated in the example below.

Create the file `STLUser.hpp`:

```
#pragma once

#include <string>
#include <vector>

inline std::string ReverseString( std::string const &s )
{
  std::string result;
  for ( std::string::const_reverse_iterator it = s.rbegin(); it != s.rend(); ++it )
    result.push_back( *it );
  return result;
}

template<typename Ty>
std::vector<Ty> ReverseVector( std::vector<Ty> const &v )
{
  std::vector<Ty> result;
  for ( typename std::vector<Ty>::const_reverse_iterator it = v.rbegin(); it != v.rend(); ++it )
    result.push_back( *it );
  return result;
}
```

Discover, generate and compile the extension:

```
path/to/kludge discover STLUser STLUser.hpp
path/to/kludge generate STLUser STLUser.kludge.py
scons -f STLUser.SConstruct
```

Test this example with the file `test.kl`:

```
require STLUser;
operator entry() {
  report(ReverseString("Hello, world!"));
}
```

Running it as usual will produce the output:

```
!dlrow ,olleH
```

What about the function `ReverseVector`?  If we try the following `test.kl`:

```
require STLUser;
operator entry() {
  SInt32 a[];
  for (SInt32 i = 0; i < 10; ++i)
    a.push(i);
  report("a = " + a);
  report("ReverseVector(a) = " + ReverseVector(a));
}
```

you will get an error that `ReverseVector` is not defined.  The problem here was already alluded to in the introduction: there is no support for templates in KL, and as such you need to explicitly add instantiations of templates you are interested in to the `.kludge.py` files. 

To do this, edit the file `STLUser.defns.kludge.py` and add the following lines to the end:

```
for ty in ['int']:
  ext.add_func('ReverseVector', 'std::vector<%s>'%ty, ['std::vector<%s> const &'%ty])
```

Now try to run `test.kl`.  You will get a different error this time, that there is no function `ReverseVector(SInt32[])`.  This is because, unlike for strings, there is no automatic conversion of KL vectors to STL vectors.  Instead, you must do this explicitly.  Change `test.kl` to:

```
require STLUser;
operator entry() {
  SInt32 a[];
  for (SInt32 i = 0; i < 10; ++i)
    a.push(i);
  report("a = " + a);
  CxxSInt32StdVector stl_a = Make_CxxSInt32StdVector(a);
  CxxSInt32StdVector stl_ra = ReverseVector(stl_a);
  SInt32 ra[] = Make_SInt32VariableArray(stl_ra);
  report("ReverseVector(a) = " + ra);
}
```

This patten of using a `Make_...` function to explicitly convert types in Kludge extensions is one that you will frequently see.  The reasons this is necessary in certain cases are a combination of limitations in KL as well as the undesirability of automatic conversions in many cases, where the conversion can be slow or have side effects; we will talk a bit more about this in the next section.

When run you should see the output:

```
a = [0,1,2,3,4,5,6,7,8,9]
ReverseVector(a) = [9,8,7,6,5,4,3,2,1,0]
```

Next: [Tutorial: More About Using C++ Types](tutorial-more-cxx-types.md)
