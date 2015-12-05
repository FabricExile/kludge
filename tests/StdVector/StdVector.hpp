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

inline std::vector< std::vector<std::string> > ReturnStringArrayArray()
{
  std::vector<std::string> b;
  b.push_back("hello");
  b.push_back("there");
  b.push_back("my");
  b.push_back("friend");

  std::vector< std::vector<std::string> > a;
  a.push_back(b);
  a.push_back(b);
  a.push_back(b);

  return a;
}

inline std::vector<double *> ReturnDoublePtrArray()
{
  std::vector<double *> result;
  static double pi = 3.14;
  result.push_back(&pi);
  result.push_back(&pi);
  result.push_back(&pi);
  return result;
}

#endif
