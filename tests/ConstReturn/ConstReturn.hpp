#ifndef _ConstReturn_HPP
#define _ConstReturn_HPP

class MyClass
{
  int a;
public:
  MyClass() {}
  const MyClass *getConst() { return const_cast<const MyClass *>(this); }
};

const MyClass *GetMyClass()
{
  return 0;
}

#endif
