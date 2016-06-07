#ifndef _Inheritance_HPP
#define _Inheritance_HPP

class SimpleParent
{
public:
  SimpleParent(int _a) { a = _a; }
  virtual int getA() { return a; }
  virtual int getSum() { return a; }

protected:
  int a;
};

class SimpleChild : public SimpleParent
{
public:
  SimpleChild(int _a, int _b) : SimpleParent(_a) { b = _b; }
  virtual int getB() { return b; }
  virtual int getSum() { return a + b; }

protected:
  int b;
};

class NoMemberParent
{
public:
  NoMemberParent(int _a) { a = _a; }
  virtual int getA() { return a; }
  virtual int getSum() { return a; }

protected:
  int a;
};

class NoMemberChild : public NoMemberParent
{
public:
  NoMemberChild(int _a) : NoMemberParent(_a) {}
  virtual int getAPlusFive() { return a + 5; }
};

class AbstractParent
{
public:
  virtual void doNothing() = 0;
};

class AbstractChild : public AbstractParent
{
public:
  void doMoreNothing() {}
};

class NotAbstract : public AbstractChild
{
public:
  virtual void doNothing() {}
  //AbstractParent getParent() { return *this; }
};

void TakesAbstract( AbstractParent *p ) {}

#endif
