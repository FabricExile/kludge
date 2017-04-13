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

    virtual bool equals(const CloneMethodClass & other) const
    {
      return true;
    }
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

    virtual bool equals(const CloneMethodClass & other) const
    {
      return true;
    }
  };
};
