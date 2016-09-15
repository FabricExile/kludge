//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

#include <iostream>
#include <assert.h>

template<typename Ty>
class Wrapper
{
public:

  Wrapper()
    : m_ptr( 0 )
  {
    std::cout << "Wrapper::Wrapper()\n" << std::flush;
  }
  Wrapper( Ty *ptr )
    : m_ptr( ptr )
  {
    std::cout << "Wrapper::Wrapper(Ty *)\n" << std::flush;
    if ( m_ptr ) m_ptr->retain();
  }
  Wrapper( Wrapper const &that )
    : m_ptr( that.m_ptr )
  {
    std::cout << "Wrapper::Wrapper(Wrapper const &)\n" << std::flush;
    if ( m_ptr ) m_ptr->retain();
  }
  ~Wrapper()
  {
    std::cout << "Wrapper::~Wrapper()\n" << std::flush;
    if ( m_ptr ) m_ptr->release();
  }

  Wrapper &operator=( Wrapper const &that )
  {
    std::cout << "Wrapper::operator=(Wrapper const &)\n" << std::flush;
    if ( m_ptr )
      m_ptr->release();
    m_ptr = that.m_ptr;
    if ( m_ptr )
      m_ptr->retain();
  }

  Ty *operator->()
    { return m_ptr; }
  Ty const *operator->() const
    { return m_ptr; }

private:

  Ty *m_ptr;
};

class RefCounter
{
public:

  RefCounter()
    : pri_refCount( 0 )
    {}
  virtual ~RefCounter() {}

  void retain()
    { ++pri_refCount; }
  void release()
    { if ( --pri_refCount == 0 ) delete this; }

private:

  int pri_refCount;
};

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
