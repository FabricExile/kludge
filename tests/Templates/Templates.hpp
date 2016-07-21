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

  Ty const &constRef()
    { return m_re; }

  void takesTemplType(const Template &tmpl) {}

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

  template<typename Ty>
  class NSTemplate
  {
  public:

    NSTemplate() {}
    NSTemplate( Ty re )
      : m_re( re )
      {}
    ~NSTemplate() {}

    Ty re()
      { return m_re; }

  private:

    Ty m_re;
  };

  typedef NSTemplate<int> NSTemplate1;
}

// [FIXME] template with explicit namespace
//typedef Myspace::NSTemplate<int> NSTemplate2;

class DerivedTempl : public Template<int, double>
{
};

class UsesTempl
{
public:
  Template32 getTempl32()
  {
    Template32 t(3.14);
    return t;
  };

  Template32 &getTempl32Ref()
  {
    static Template32 t(3.14);
    return t;
  };

};

#endif
