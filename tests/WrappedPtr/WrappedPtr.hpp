#ifndef _WrappedPtr_HPP
#define _WrappedPtr_HPP

#include <stdio.h>
#include <string>
#include <vector>

class Class {
public:

  Class() {}
  Class(
    float _floatValue,
    std::string const &_stringValue,
    int _intValue
    )
    : floatValue( _floatValue )
    , stringValue( _stringValue )
    , pri_intValue( _intValue )
    {}
  Class( Class const &that )
    : floatValue( that.floatValue )
    , stringValue( that.stringValue )
    , pri_intValue( that.pri_intValue )
    {}
  ~Class() {}

  Class &operator=( Class const &that )
  {
    floatValue = that.floatValue;
    stringValue = that.stringValue;
    pri_intValue = that.pri_intValue;
    return *this;
  }

  static void PrintValues( Class const &that )
  {
    printf("%.2f %s %d\n", that.floatValue, that.stringValue.c_str(),
           that.pri_intValue);
  }

  void changeValues( Class &that )
  {
    floatValue = that.floatValue;
    stringValue = that.stringValue;
    pri_intValue = that.pri_intValue;
  }

  std::string const &publicMethod() { return stringValue; }

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

Class ReturnClass() {
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

#endif
