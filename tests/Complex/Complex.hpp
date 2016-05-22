#ifndef COMPLEX_HPP
#define COMPLEX_HPP

namespace TestNameSpace {

template<typename Ty, typename Ty2>
class Complex
{
public:

  Complex() {}
  Complex( Ty const &re )
    : m_re( re )
    , m_im( 0 )
    {}
  Complex( Ty const &re, Ty const &im )
    : m_re( re )
    , m_im( im )
    {}
  Complex( Complex const &that )
    : m_re( that.m_re )
    , m_im( that.m_im )
    {}
  ~Complex() {}

  Complex &operator=( Complex const &that )
  {
    m_re = that.m_re;
    m_im = that.m_im;
    return *this;
  }

  Ty const &re() const
    { return m_re; }

  Ty const &im() const
    { return m_im; }

private:

  Ty m_re, m_im;
  Ty2 m_other;
  bool m_nontemplate;
};

typedef Complex<float, int> Complex32;
// typedef Complex<double> Complex64;

/*
class A
{
public:
  Complex<double, bool> foo;
};
*/

}

#endif
