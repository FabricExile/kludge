#ifndef _MultiFileParent_HPP
#define _MultiFileParent_HPP

class MultiParent
{
public:
  MultiParent(int _a) { a = _a; }
  virtual int getA() { return a; }
  virtual int getSum() { return a; }

protected:
  int a;
};

class MethodRet
{
public:
  MethodRet() : a(0) {}
  int a;
};

class MethodParm
{
public:
  MethodParm() : a(0) {}
  int a;
};

class ConstructParam
{
public:
  ConstructParam() : a(0) {}
  int a;
};

class Member
{
public:
  Member() : a(0) {}
  int a;
};

#endif
