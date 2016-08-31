#pragma once

#include <iostream>
#include <stdio.h>
#include <string>
#include <vector>

template<typename Ty>
class Wrapper
{
public:

  Wrapper()
    : m_ptr( 0 ) {}
  Wrapper( Ty *ptr )
    : m_ptr( ptr )
    { if ( m_ptr ) m_ptr->retain(); }
  Wrapper( Wrapper const &that )
    : m_ptr( that.m_ptr )
    { if ( m_ptr ) m_ptr->retain(); }
  ~Wrapper()
    { if ( m_ptr ) m_ptr->release(); }

  Wrapper &operator=( Wrapper const &that )
  {
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

class Class {
public:

  Class() : pri_refCount( 0 )
  {
    std::cout << "Class::Class()\n" << std::flush;
  }
  Class(
    float _floatValue,
    std::string const &_stringValue,
    int _intValue
    )
    : pri_refCount( 0 )
    , floatValue( _floatValue )
    , stringValue( _stringValue )
    , pri_intValue( _intValue )
  {
    std::cout << "Class::Class(" << _floatValue << ", " << _stringValue << ", " << _intValue << ")\n" << std::flush;
  }
  ~Class()
  {
    std::cout << "Class::~Class()\n" << std::flush;
  }

  void retain()
    { ++pri_refCount; }
  void release()
    { if ( --pri_refCount == 0 ) delete this; }

  std::string const &publicMethod() { return stringValue; }

private:

  mutable int pri_refCount;

public:

  float floatValue;
  std::string stringValue;

private:

  int pri_intValue;
};
