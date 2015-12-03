#ifndef _Functions_hpp
#define _Functions_hpp

#include <string>
#include <vector>
#include <stdint.h>

namespace SomeNameSpace {

namespace SomeNestedNameSpace {

inline void TestStdString(
  std::string strVal,
  std::string const &strConstRef,
  std::string &strMutableRef,
  std::string const *strConstPtr,
  std::string *strMutablePtr
  ) {}

inline void TestCString(
  char const *cStringVal,
  char const * const &CStringConstRef
  ) {}

inline int TestSimpleValueReturn() { return 42; }
inline int const &TestSimpleConstRefReturn() { static int foo = 42; return foo; }
inline int &TestSimpleMutableRefReturn() { static int foo = 42; return foo; }

inline std::string TestStdStringValueReturn() { return "hello"; }
inline std::string const &TestStdStringConstRefReturn() { static std::string foo = "hello"; return foo; }
inline std::string &TestStdStringMutableRefReturn() { static std::string foo = "hello"; return foo; }

inline char const * TestCStringValueReturn() { return "hello"; }
inline char const * const &TestCStringConstRefReturn() { static char const *foo = "hello"; return foo; }

inline float ReturnSecond( std::vector<float> const &vals ) { return vals[1]; }

inline char const * ReturnSecondSecond( std::vector< std::vector<char const *> > const &vals ) { return vals[1][1]; }

}

inline float Sum( float lhs, float rhs ) { return lhs + rhs; }

}

#endif
