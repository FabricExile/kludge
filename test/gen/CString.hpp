//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

#include <string>

inline const char *CStringParams(
  char const *cStringValue,
  char const * const &cStringConstRef
  )
{
  static std::string foo;
  foo = cStringValue;
  foo += cStringConstRef;
  return foo.c_str();
}

inline char const *CStringValueReturn() { return "value"; }
inline char const * const &CStringConstRefReturn() { static char const *foo = "constRef"; return foo; }
