#ifndef _WrappedPtr_HPP
#define _WrappedPtr_HPP

#include <stdio.h>
#include <string>
#include <vector>

class Class {
public:

  Class() {}
  Class( float pub, std::string const &pri )
    : m_pub( pub )
    , m_pri( pri )
    {}
  Class( Class const &that )
    : m_pub( that.m_pub )
    , m_pri( that.m_pri )
    {}
  ~Class() {}

  Class &operator=( Class const &that )
  {
    m_pub = that.m_pub;
    m_pri = that.m_pri;
    return *this;
  }

  std::string const &publicMethod() { return m_pri; }

  std::string getDesc() const {
    return "pri: " + m_pri;
  }

protected:

  std::string const &protectedMethod() { return m_pri; }

private:

  std::string const &privateMethod() { return m_pri; }

public:

  float m_pub;

private:

  std::string m_pri;
};

Class ReturnClass() {
  return Class( 5.61, "foo" );
}

std::vector<Class> ReturnClassVec() {
  std::vector<Class> result;
  result.push_back( Class( 1.2, "bar" ) );
  result.push_back( Class( -97.1, "baz" ) );
  return result;
}

#endif
