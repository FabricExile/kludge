//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

#include <iostream>
#include <stdio.h>
#include <string>
#include <vector>

class MyOpaque;
class MyOpaqueDer;

struct MyOpaque_Real
{
  int x;

  virtual ~MyOpaque_Real() {}
};

struct MyOpaqueDer_Real : public MyOpaque_Real
{
  float y;
};

inline MyOpaque *MyOpaque_New( int x )
{
  MyOpaque_Real *r = new MyOpaque_Real;
  r->x = x;
  return reinterpret_cast<MyOpaque *>( r );
}

inline void MyOpaque_New_Alt( int x, MyOpaque **result )
{
  *result = MyOpaque_New( x );
}

inline int MyOpaque_GetX( MyOpaque const *_r )
{
  MyOpaque_Real const *r = reinterpret_cast<MyOpaque_Real const *>( _r );
  return r->x;
}

inline void MyOpaque_SetX( MyOpaque *_r, int x )
{
  MyOpaque_Real *r = reinterpret_cast<MyOpaque_Real *>( _r );
  r->x = x;
}

inline MyOpaque const * MyOpaque_ReturnConstPtr( MyOpaque const *_r )
{
  return _r;
}

inline void MyOpaque_Delete( MyOpaque *_r )
{
  MyOpaque_Real *r = reinterpret_cast<MyOpaque_Real *>( _r );
  delete r;
}

inline MyOpaqueDer *MyOpaqueDer_New( int x, float y )
{
  MyOpaqueDer_Real *r = new MyOpaqueDer_Real;
  r->x = x;
  r->y = y;
  return reinterpret_cast<MyOpaqueDer *>( r );
}

inline float MyOpaqueDer_GetY( MyOpaqueDer const *_r )
{
  MyOpaqueDer_Real const *r = reinterpret_cast<MyOpaqueDer_Real const *>( _r );
  return r->y;
}

inline void MyOpaqueDer_SetY( MyOpaqueDer *_r, float y )
{
  MyOpaqueDer_Real *r = reinterpret_cast<MyOpaqueDer_Real *>( _r );
  r->y = y;
}

inline void MyOpaqueDer_Delete( MyOpaqueDer *_r )
{
  MyOpaqueDer_Real *r = reinterpret_cast<MyOpaqueDer_Real *>( _r );
  delete r;
}
