#ifndef _CLASS_HPP
#define _CLASS_HPP

namespace SomeNameSpace {
namespace NestedNameSpace {

class Class {
public:

  Class() {}
  Class( float x ) : m_x( x ) {}
  Class( Class const &that ) : m_x( that.m_x ) {}
  ~Class() {}

  Class &operator=( Class const &that )
  {
    m_x = that.m_x;
    return *this;
  }

  float publicMethod() { return m_x; }

protected:

  float protectedMethod() { return m_x; }

private:

  float privateMethod() { return m_x; }

  float m_x;
};

} }

#endif
