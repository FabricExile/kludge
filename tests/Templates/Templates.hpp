#ifndef TEMPLATES_HPP
#define TEMPLATES_HPP

template<typename Ty, typename Ty2>
class Template
{
public:

  Template() {}
  Template( Ty re )
    : m_re( re )
    {}
  ~Template() {}

  Ty re()
    { return m_re; }

private:

  Ty m_re;
  Ty2 m_other;
  bool m_nontemplate;
};

typedef Template<float, int> Template32;
typedef Template<bool, double> TemplateBool;

class InlineType
{
public:
  InlineType() : m_foo( 5 ) {}

  int getFooRe()
  {
    return m_foo.re();
  }

private:
  Template<int, int> m_foo;
};

struct MyType1
{
  int a;
};

namespace Myspace
{
  struct MyType2
  {
    int a;
  };

  typedef Template<MyType1, int> MyspaceType1;
  typedef Template<MyType2, int> MyspaceType2;
}

#endif
