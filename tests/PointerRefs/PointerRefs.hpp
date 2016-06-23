#ifndef _PointerRefs_HPP
#define _PointerRefs_HPP

class SimpleClass
{
  int m_x;

public:
  SimpleClass() : m_x(0) {}

  void setX(int x)
  {
    m_x = x;
  }

  int getX()
  {
    return m_x;
  }
};

class PointerRef
{
  int *m_x;
  SimpleClass *m_s;

public:
  PointerRef() : m_x(0), m_s(new SimpleClass()) {}

  int * &getXRef()
  {
    return m_x;
  }

  SimpleClass getS()
  {
    return *m_s;
  }

  SimpleClass *getSPtr()
  {
    return m_s;
  }

  SimpleClass &getSRef()
  {
    return *m_s;
  }

  SimpleClass * &getSPtrRef()
  {
    return m_s;
  }
};

class NullPointer
{
public:
  NullPointer *getNull()
  {
    return 0;
  }
};

#endif
