#ifndef _MultiFile_HPP
#define _MultiFile_HPP

#include "subdir/MultiFileParent.hpp"

class MultiChild : public MultiParent
{
public:
  MultiChild(int _a, int _b) : MultiParent(_a) { b = _b; }
  MultiChild(ConstructParam c) : MultiParent(5) { }
  virtual int getB() { return b; }
  virtual int getSum() { return a + b; }
  MethodRet getRet() { return MethodRet(); }
  int getParmA(MethodParm p) { return p.a; }

protected:
  int b;
};

#endif
