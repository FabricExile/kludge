//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

#include <iostream>
#include <stdio.h>
#include <string>
#include <vector>
#include <assert.h>
#include "Wrapper.hpp"

class Class : public RefCounter
{
private:

  Class()
  {
    assert( false );
  }
  Class( Class const &that )
  {
    assert( false );
  }
  Class &operator=(Class const &that)
  {
    assert( false );
    return *this;
  }

public:

  Class(
    float _floatValue,
    std::string const &_stringValue,
    int _intValue
    )
    : floatValue( _floatValue )
    , stringValue( _stringValue )
    , pri_intValue( _intValue )
  {
    std::cout << "Class::Class(" << _floatValue << ", " << _stringValue << ", " << _intValue << ")\n" << std::flush;
  }
  ~Class()
  {
    std::cout << "Class::~Class()\n" << std::flush;
  }

  Class const *unwrap() const
  {
    return this;
  }

  static void PrintValues( Class const *that )
  {
    printf("%.2f %s %d\n", that->floatValue, that->stringValue.c_str(),
           that->pri_intValue);
    fflush( stdout );
  }

  static void PrintValues( Wrapper<Class> const &that )
  {
    PrintValues( that.operator->() );
  }

  int operator[]( size_t index ) const
  {
    std::cout<< "Class::operator[] const(" << index << ")\n" << std::flush;
    return pri_intValue;
  }

  int &operator[]( size_t index )
  {
    std::cout<< "Class::operator[](" << index << ")\n" << std::flush;
    return pri_intValue;
  }

  std::string const &publicMethod() { return stringValue; }

  int getIntValue() const
    { return pri_intValue; }

public:

  float floatValue;
  std::string stringValue;

private:

  int pri_intValue;
};

inline int GlobalGetIntValue( Class const &klass ) {
  return klass.getIntValue();
}

class DerivedClass : public Class
{
public:

  DerivedClass(
    int _intValue
    )
    : Class( 3.14, "hello", _intValue )
  {
    std::cout << "DerivedClass::DerivedClass(" << _intValue << ")\n" << std::flush;
  }

  ~DerivedClass()
  {
    std::cout << "DerivedClass::~DerivedClass()\n" << std::flush;
  }

  int newMethod() const
    { return -9; }
};
