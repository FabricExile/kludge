#ifndef OPDEREF_HPP
#define OPDEREF_HPP

template<typename Ty>
class Wrapper
{
public:

  Wrapper() : m_ty() {}

  Ty *operator->()
  {
    return &m_ty;
  }

  operator Ty *()
  {
    return &m_ty;
  }

  int getSix()
  {
    return 6;
  }

private:

  Ty m_ty;
};

class MyType
{
public:
  MyType() {}
  int getFive() { return 5; }
  float getPI() { return 3.14; }
};

typedef Wrapper<MyType> MyTypePtr;

#endif
