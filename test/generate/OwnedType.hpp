//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

#include <iostream>
#include <stdio.h>
#include <string>
#include <vector>

class Class {
public:

  Class() {}
  Class( std::string const &_stringValue )
    : floatValue( -6.34 )
    , stringValue( _stringValue )
    , pri_intValue( -7 )
  {
    std::cout << "Class::Class(" << _stringValue << ")\n" << std::flush;
  }
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
  Class( Class const &that )
    : floatValue( that.floatValue )
    , stringValue( that.stringValue )
    , pri_intValue( that.pri_intValue )
  {
    std::cout << "Class::Class(Class const &)\n" << std::flush;
  }
  ~Class()
  {
    std::cout << "Class::~Class()\n" << std::flush;
  }

  Class &operator=( Class const &that )
  {
    std::cout << "Class::operator=(Class const &)\n" << std::flush;
    floatValue = that.floatValue;
    stringValue = that.stringValue;
    pri_intValue = that.pri_intValue;
    return *this;
  }

  static void PrintValues( Class const &that )
  {
    printf("%.2f %s %d\n", that.floatValue, that.stringValue.c_str(),
           that.pri_intValue);
    fflush( stdout );
  }

  void changeValues( Class &that )
  {
    floatValue = that.floatValue;
    stringValue = that.stringValue;
    pri_intValue = that.pri_intValue;
  }

  void operator()( int foo )
  {
    std::cout << "Class::operator()(" << foo << ")\n" << std::flush;
  }

  std::string const &publicMethod() { return stringValue; }

  int getIntValue() const { return pri_intValue; }

  std::string getDesc() const {
    return "stringValue: " + stringValue;
  }

  float getMulFloatValue( float x ) const { return x * floatValue; }

  void exportValues(
    float &_floatValue,
    std::string &_stringValue,
    int &_intValue
    )
  {
    _floatValue = floatValue;
    _stringValue = stringValue;
    _intValue = pri_intValue;
  }

  operator bool() const
    { return !!pri_intValue; }

  Class &operator ++()
    { ++pri_intValue; return *this; }

  int const &operator*() const
    { return pri_intValue; }

  Class operator+( Class const &that ) const
  {
    return Class(
      floatValue + that.floatValue,
      stringValue + that.stringValue,
      pri_intValue + that.pri_intValue
      );
  }

  Class &operator+=( Class const &that )
  {
    floatValue += that.floatValue;
    stringValue += that.stringValue;
    pri_intValue += that.pri_intValue;
    return *this;
  }

  int data() const { return 432; }

protected:

  std::string const &protectedMethod() { return stringValue; }

private:

  std::string const &privateMethod() { return stringValue; }

public:

  float floatValue;
  std::string stringValue;

private:

  int pri_intValue;
};

inline void GlobalFuncTakingClassConstRef( Class const &klass ) {
  std::cout << "GlobalFuncTakingClassConstRef: klass.stringValue = " + klass.stringValue + "\n" << std::flush;
}

inline Class operator*( Class const &lhs, Class const &rhs ) {
  return Class(
    lhs.floatValue * rhs.floatValue,
    lhs.stringValue + rhs.stringValue,
    lhs.getIntValue() * rhs.getIntValue()
    );
}

inline Class ReturnClass() {
  return Class( 5.61, "foo", -43 );
}

std::vector<Class> ReturnClassVec() {
  std::vector<Class> result;
  result.push_back( Class( 1.2, "bar", 64 ) );
  result.push_back( Class( -97.1, "baz", 164 ) );
  return result;
}

struct StructWithIndirectTypeThatCanInPlace {
  StructWithIndirectTypeThatCanInPlace( float const &x )
    : floatValue( x ) {}
  float const &floatValue;
};

StructWithIndirectTypeThatCanInPlace ReturnStructWithIndirectTypeThatCanInPlace() {
  static float x = 5.76;
  return StructWithIndirectTypeThatCanInPlace( x );
}

class DerivedClass : public Class
{
public:

  DerivedClass(
    int _intValue
    )
    : Class( 3.14, "hello", _intValue )
    , newPublicMember(2.81)
  {
    std::cout << "DerivedClass::DerivedClass(" << _intValue << ")\n" << std::flush;
  }

  ~DerivedClass()
  {
    std::cout << "DerivedClass::~DerivedClass()\n" << std::flush;
  }

  int newMethod() const
    { return -9; }

  double newPublicMember;
};
