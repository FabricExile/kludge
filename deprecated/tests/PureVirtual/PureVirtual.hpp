#ifndef _PureVirtual_HPP
#define _PureVirtual_HPP

class Normal {
public:
  Normal() {}
  virtual void mymethod() {}
  int myint;
};

class PureVirt {
public:
  PureVirt() {}
  virtual void mymethod() = 0;
  int myint;
};

#endif
