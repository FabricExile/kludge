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
  Template( Template const &that )
    : m_re( that.m_re )
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
// typedef Template<double> Template64;

/*
class InlineType
{
public:
  Template<double, bool> foo;
};
*/

#endif
