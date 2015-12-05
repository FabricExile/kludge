#ifndef _StdVector_hpp
#define _StdVector_hpp

#include <string>
#include <map>

inline float ReturnValueForKey(
  std::map<float, float> const &vals,
  float key
  )
{
  std::map<float, float>::const_iterator it = vals.find( key );
  return it->second;
}

inline char const *ReturnValueForKeyKey(
  std::map< unsigned, std::map<std::string, char const *> > const &vals,
  unsigned key1,
  std::string const &key2
  )
{
  std::map< unsigned, std::map<std::string, char const *> >::const_iterator it = vals.find( key1 );
  std::map<std::string, char const *>::const_iterator jt = it->second.find( key2 );
  return jt->second;
}

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
