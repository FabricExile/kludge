//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

class MyAbstractClass
{
public:
  MyAbstractClass() {}
  virtual const char *GetData(int index) const = 0;
  virtual const char *GetData() const
  {
    return "MyAbstractClass";
  }
};
