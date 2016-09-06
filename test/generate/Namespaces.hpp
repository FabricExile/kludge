//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

#include <iostream>
#include <assert.h>
#include "Wrapper.hpp"

inline char const *GlobalFunc() {
  return "From root namespace";
}

namespace NameSpace {

class Class : public RefCounter
{
public:

  class SubClass
  {
  public:

    SubClass() {}

    SubClass( int theX )
      : x( theX )
      {}

    int x;
  };

  Class( int x )
    : _subClass( x )
    {}

  SubClass const &getSubClass() const
    { return _subClass; }

  enum Enum { Foo, Bar };

  static char const *DescEnum( Enum en )
  {
    switch ( en )
    {
      case Foo: return "Foo";
      case Bar: return "Bar";
      default: assert(false); return "**UNKNOWN**";
    }
  }

private:

  SubClass _subClass;
};

inline char const *GlobalFunc() {
  return "From NameSpace";
}

namespace NestedNameSpace {

inline char const *GlobalFunc() {
  return "From NestedNameSpace";
}

} // namespace NestedNameSpace

} // namespace NameSpace
