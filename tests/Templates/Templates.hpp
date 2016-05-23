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

#endif
