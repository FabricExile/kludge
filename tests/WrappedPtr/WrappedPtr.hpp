#ifndef _WrappedPtr_HPP
#define _WrappedPtr_HPP

#include <stdio.h>
#include <string>
#include <vector>

class Class {
public:

  Class() {}
  Class( std::string const &str ) : m_str( str ) {}
  Class( Class const &that ) : m_str( that.m_str ) {}
  ~Class() {}

  Class &operator=( Class const &that )
  {
    m_str = that.m_str;
    return *this;
  }

  std::string const &publicMethod() { return m_str; }

  std::string getDesc() const {
    return "str: " + m_str;
  }

protected:

  std::string const &protectedMethod() { return m_str; }

private:

  std::string const &privateMethod() { return m_str; }

  std::string m_str;
};

Class ReturnClass() {
  return Class( "foo" );
}

std::vector<Class> ReturnClassVec() {
  std::vector<Class> result;
  result.push_back( Class( "bar" ) );
  result.push_back( Class( "baz" ) );
  return result;
}

#endif
