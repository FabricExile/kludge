#ifndef _StdString_hpp
#define _StdString_hpp

#include <string>

inline void StdStringParams(
  std::string value,
  std::string const &constRef,
  //std::string const *constPtr,
  std::string &mutableRef
  //std::string *mutablePtr
  )
{
  mutableRef += value;
  mutableRef += constRef;
  //*mutablePtr += *constPtr;
}

inline std::string StdStringValueReturn() { return "value"; }
inline std::string const &StdStringConstRefReturn() { static std::string foo = "constRef"; return foo; }
inline std::string &StdStringMutableRefReturn() { static std::string foo = "constPtr"; return foo; }

#endif
