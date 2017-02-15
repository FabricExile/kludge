//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

#include <iostream>

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
    return *this;
  }

  bool operator!() const
    { return !m_ptr; }
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
