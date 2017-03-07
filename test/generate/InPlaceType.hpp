//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

#include <stdio.h>
#include <iostream>
#include <string>
#include <vector>

class Class {
public:

  Class()
  {
    std::cout<< "Class::Class()\n" << std::flush;
  }
  Class( int _intValue, float _floatValue )
    : intValue( _intValue ), floatValue( _floatValue ) 
  {
    std::cout<< "Class::Class(" << _intValue << ", " << _floatValue << ")\n" << std::flush;
  }
  Class( Class const &that )
    : intValue( that.intValue ), floatValue( that.floatValue )
  {
    std::cout<< "Class::Class(Class const &)\n" << std::flush;
  }
  ~Class()
  {
    std::cout<< "Class::~Class()\n" << std::flush;
  }

  Class &operator=( Class const &that )
  {
    std::cout<< "Class::operator=(Class const &)\n" << std::flush;
    intValue = that.intValue;
    floatValue = that.floatValue;
    return *this;
  }

  float publicConstMethod() const { return floatValue; }
  float publicMutableMethod() { return floatValue; }

  void publicVoidConstMethod() const {}
  void publicVoidMutableMethod() {}

  std::string getDesc() const {
    char buf[256];
    snprintf( buf, 256, "intValue:%d floatValue:%f", intValue, floatValue );
    return std::string( buf );
  }

  static float GetStaticFloat() { return 3.3; }

  int operator[]( size_t index ) const
  {
    std::cout<< "Class::operator[] const(" << index << ")\n" << std::flush;
    return intValue;
  }

  int &operator[]( size_t index )
  {
    std::cout<< "Class::operator[](" << index << ")\n" << std::flush;
    return intValue;
  }

protected:

  float protectedMethod() { return floatValue; }

private:

  float privateMethod() { return floatValue; }

public:

  int intValue;

private:

  float floatValue;
};

Class ReturnClass() {
  return Class( 92, 6.74 );
}

std::vector<Class> ReturnClassVec() {
  std::vector<Class> result;
  result.push_back( Class( 3, 3.14 ) );
  result.push_back( Class( -14, -3.45 ) );
  return result;
}

class DerivedClass : public Class
{
public:
  
  DerivedClass()
  {
    std::cout<< "DerivedClass::DerivedClass()\n" << std::flush;
  }
  DerivedClass( int _intValue, float _floatValue, short _shortValue )
    : Class( _intValue, _floatValue )
    , shortValue( _shortValue )
  {
    std::cout<< "DerivedClass::DerivedClass(" << _intValue << ", " << _floatValue << ", " << _shortValue << ")\n" << std::flush;
  }
  DerivedClass( DerivedClass const &that )
    : Class( that )
    , shortValue( that.shortValue )
  {
    std::cout<< "DerivedClass::DerivedClass(DerivedClass const &)\n" << std::flush;
  }
  ~DerivedClass()
  {
    std::cout<< "DerivedClass::~DerivedClass()\n" << std::flush;
  }

  DerivedClass &operator=( DerivedClass const &that )
  {
    std::cout<< "DerivedClass::operator=(DerivedClass const &)\n" << std::flush;
    *(Class *)this = (Class const &)that;
    shortValue = that.shortValue;
    return *this;
  }

  short anotherPublicMethod() const { return shortValue * -3; }

public:

  short shortValue;
};

template<typename Ty>
class InPlaceTypeTester
{
public:
  Ty value;

  InPlaceTypeTester() : value( 0 ) {}
  InPlaceTypeTester( Ty m ) : value( m ) {}
  
  Ty get() const { return value; }
  void set( Ty m ) { value = m; }
};

typedef InPlaceTypeTester< char > InPlaceTypeTesterChar;
typedef InPlaceTypeTester< int > InPlaceTypeTesterInt;
typedef InPlaceTypeTester< unsigned int > InPlaceTypeTesterUInt;
typedef InPlaceTypeTester< long long > InPlaceTypeTesterLongLong;
typedef InPlaceTypeTester< unsigned long long > InPlaceTypeTesterULongLong;
typedef InPlaceTypeTester< uint8_t > InPlaceTypeTesterUInt8T;
typedef InPlaceTypeTester< uint16_t > InPlaceTypeTesterUInt16T;
typedef InPlaceTypeTester< uint32_t > InPlaceTypeTesterUInt32T;
typedef InPlaceTypeTester< size_t > InPlaceTypeTesterSizeT;
