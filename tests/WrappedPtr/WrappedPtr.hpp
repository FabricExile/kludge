#ifndef _WrappedPtr_HPP
#define _WrappedPtr_HPP

class WrappedPtr {
public:

  WrappedPtr() {}
  WrappedPtr( float x ) : m_x( x ) {}
  WrappedPtr( WrappedPtr const &that ) : m_x( that.m_x ) {}
  ~WrappedPtr() {}

  WrappedPtr &operator=( WrappedPtr const &that )
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

WrappedPtr ReturnWrappedPtr() {
  return WrappedPtr( 6.74 );
}

#endif
