//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

#include <iostream>
#include <stdio.h>
#include <string>
#include <vector>
#include <stdexcept>

class Class {
public:

  Class() {}

  void publicMethod( std::string const &str ) {
    if(str.length() == 0)
      throw std::runtime_error("publicMethod: Empty string");
  }
};
