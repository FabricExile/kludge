#ifndef _StdMap_hpp
#define _StdMap_hpp

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

inline std::map< char const *, std::map<float, std::string> > ReturnNestedMap()
{
  std::map<float, std::string> m1;
  m1[-6.54] = "asdf";
  m1[2.31] = "qowe";
  
  std::map<float, std::string> m2;
  m2[1.56] = "vibawe";
  m2[-2.31] = "asdvi";
  
  std::map< char const *, std::map<float, std::string> > m;
  m["foo"] = m1;
  m["bar"] = m2;

  return m;
}

#endif
