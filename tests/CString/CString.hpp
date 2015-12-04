#ifndef _CString_hpp
#define _CString_hpp

inline void CStringParams(
  char const *cStringValue,
  char const * const &cStringConstRef
  ) {}

inline char const *CStringValueReturn() { return "hello"; }
inline char const * const &CStringConstRefReturn() { static char const *foo = "hello"; return foo; }

#endif
