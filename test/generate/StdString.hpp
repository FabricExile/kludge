//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

#include <string>

inline std::string ReturnStdString()
{
  return std::string("foo");
}

inline std::string const &ReturnStdStringConstRef()
{
  static std::string ss("foo");
  return ss;
}
