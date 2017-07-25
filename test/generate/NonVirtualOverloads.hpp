#include <errno.h>

class BaseClass
{
public:

  BaseClass(int i)
  : m_i(i)
  {

  }

  bool Reverse() const { return false; }

  void SetFrom(const BaseClass & c)
  {
  }

private:
  int m_i;
};


class Class : public BaseClass
{
public:
  Class(int i)
  : BaseClass(i)
  {}

  bool Reverse() const { return true; }

  void SetFrom(const Class & c)
  {
  }
};
