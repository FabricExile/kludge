//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

#include <iostream>

inline void FuncWithOptionalParams( int a, float b = 4.65 )
{
  std::cout << "FuncWithOptionalParams a=" << a << " b=" << b << "\n" << std::flush;
}
