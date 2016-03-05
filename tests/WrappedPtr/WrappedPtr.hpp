#ifndef _WrappedPtr_HPP
#define _WrappedPtr_HPP

#include <stdio.h>
#include <string>

class Class {
public:

  Class() {}
  Class( float x ) : m_x( x ) {}
  Class( Class const &that ) : m_x( that.m_x ) {}
  ~Class() {}

  // Class &operator=( Class const &that )
  // {
  //   m_x = that.m_x;
  //   return *this;
  // }

  float publicMethod() { return m_x; }

  std::string getDesc() const {
    char buf[20];
    snprintf( buf, 20, "%f", m_x );
    return std::string( buf );
  }

protected:

  float protectedMethod() { return m_x; }

private:

  float privateMethod() { return m_x; }

  float m_x;
};

Class ReturnClass() {
  return Class( 6.74 );
}

#endif
