//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

#include <iostream>
#include <assert.h>

enum GlobalEnum
{
  ValueZero,
  ValueOne,
  ValueTwo,
  ValueSeventeen = 17
};

void DescribeGlobalEnum( GlobalEnum e )
{
  std::cout << "DescribeGlobalEnum: e=";
  switch ( e )
  {
    case ValueZero:
      std::cout << "ValueZero";
      break;
    case ValueOne:
      std::cout << "ValueOne";
      break;
    case ValueTwo:
      std::cout << "ValueTwo";
      break;
    case ValueSeventeen:
      std::cout << "ValueSeventeen";
      break;
    default:
      assert( false );
      std::cout << "**UNKNOWN**";
      break;
  }
  std::cout << "\n" << std::flush;
}

GlobalEnum ReturnGlobalEnum()
{
  return ValueTwo;
}

void SetGlobalEnum( GlobalEnum &e )
{
  e = ValueTwo;
}
