//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

struct CxxVec2
{
  float x, y;
  CxxVec2( float _x, float _y ) : x(_x), y(_y) {}

  float dot( CxxVec2 const &that ) const
    { return x * that.x + y * that.y; }
};

inline CxxVec2 ReturnCxxVec2()
{
  return CxxVec2(-6.7, 4.2);
}

inline CxxVec2 const &ReturnCxxVec2ConstRef()
{
  static CxxVec2 vec2(1.2, -6);
  return vec2;
}

inline CxxVec2 DoubleCxxVec2( CxxVec2 const &vec2 ) {
  return CxxVec2( vec2.x + vec2.x, vec2.y + vec2.y );
}
