//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

#include <vector>

class Class
{
public:
  Class( int count )
  {
    m_v.resize(count);
  }

  int operator[]( int index ) { return m_v[index]; }
  int operator[]( unsigned int index ) { return m_v[index]; }
  int operator[]( long int index ) { return m_v[index]; }

private:
  std::vector<int> m_v;
};

