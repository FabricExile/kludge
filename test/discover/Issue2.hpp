//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

class Issue2
{
public:
  Issue2( int a ) : m_a( a ) {}
  int &operator[]( int index ) { return m_a; }
  int const &operator[]( int index ) const { return m_a; }
  int &operator*() { return m_a; };
  int const &operator*() const { return m_a; };
private:
  int m_a;
};

inline Issue2 operator*( Issue2 const &lhs, Issue2 const &rhs ) {
  return Issue2( *lhs * *rhs );
}
