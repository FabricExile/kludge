#ifndef _InPlaceStruct_HPP
#define _InPlaceStruct_HPP

#include <stdio.h>
#include <iostream>
#include <string>
#include <vector>

class Class {
public:

  Class() {}
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

  float publicMethod() { return floatValue; }

  std::string getDesc() const {
    char buf[256];
    snprintf( buf, 256, "intValue:%d floatValue:%f", intValue, floatValue );
    return std::string( buf );
  }

  static float GetStaticFloat() { return 3.3; }

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

#endif
