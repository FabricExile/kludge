//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

inline int const * const * const *GetIntCPtrCPtrCPtr()
{
  static int foo = 42;
  static int const *fooCPtr = &foo;
  static int const * const *fooCPtrCPtr = &fooCPtr;
  return &fooCPtrCPtr;
}


class Class
{
  public:

    Class() {}

    operator char const *() const { return "hello"; }
};
