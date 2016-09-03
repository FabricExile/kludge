#ifndef _ForwardDeclare_HPP
#define _ForwardDeclare_HPP

class Forward;

void TakeForward( Forward const &fwd ) {}

class Other
{
public:
  void takeForward( Forward *fwd ) {}
};

class Forward
{
  int a;
};

#endif
