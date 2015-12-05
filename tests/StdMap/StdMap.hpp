#ifndef _StdVector_hpp
#define _StdVector_hpp

#include <string>
#include <map>

inline float ReturnValue(
  std::map<float, float> const &vals,
  float key
  )
{
  std::map<float, float>::const_iterator it = vals.find( key );
  return it->second;
}

// inline char const * ReturnSecondSecond(
//   std::map< std::map<char const *> > const &vals
//   )
// {
//   return vals[1][1];
// }

// inline std::map< std::map<std::string> > ReturnStringArrayArray()
// {
//   std::map<std::string> b;
//   b.push_back("hello");
//   b.push_back("there");
//   b.push_back("my");
//   b.push_back("friend");

//   std::map< std::map<std::string> > a;
//   a.push_back(b);
//   a.push_back(b);
//   a.push_back(b);

//   return a;
// }

// inline std::map<double *> ReturnDoublePtrArray()
// {
//   std::map<double *> result;
//   static double pi = 3.14;
//   result.push_back(&pi);
//   result.push_back(&pi);
//   result.push_back(&pi);
//   return result;
// }

#endif
