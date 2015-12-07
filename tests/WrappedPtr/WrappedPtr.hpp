#ifndef _WrappedPtr_HPP
#define _WrappedPtr_HPP

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

Class ReturnClass() {
  return Class( 6.74 );
}

#endif
