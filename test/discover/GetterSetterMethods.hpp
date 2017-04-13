//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

class GetterSetterClass
{
public:

  // public members
  double x;
  int y;

  double get_x() const
  {
    return x;
  }

  void set_y(int value)
  {
    y = value;
  }
};
