//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

inline void *FunctionTakingVoidPtr( void *ptr ) { return ptr; }

class Class
{
  public:

    Class() {}

    operator void const *() const { return this; }
    operator void *() { return this; }
};
