//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

namespace ccl
{
  class CloneMethodClass
  {
  public:

    virtual CloneMethodClass *clone() const = 0;
  };

  class CloneMethodSpecialized : public CloneMethodClass
  {
  public:

    virtual CloneMethodClass *clone() const 
    { 
      return NULL;
    }

    void CopyFrom(CloneMethodSpecialized *)
    {
    }
  };
};
