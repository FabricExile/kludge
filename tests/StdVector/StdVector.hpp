#ifndef _StdVector_hpp
#define _StdVector_hpp

#include <string>
#include <vector>

inline float ReturnSecond(
  std::vector<float> const &vals
  )
{
  return vals[1];
}

inline char const * ReturnSecondSecond(
  std::vector< std::vector<char const *> > const &vals
  )
{
  return vals[1][1];
}

#endif
