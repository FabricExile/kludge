//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

#include <string>
#include <iostream>

inline std::string ReturnStdString()
{
  return std::string("foo");
}

inline std::string const &ReturnStdStringConstRef()
{
  static std::string ss("foo");
  return ss;
}

class MyType
{
public:

  MyType( std::string const &s )
    : m_s( s )
  {
    std::cout << "MyType::MyType(" << s << ")\n" << std::flush;
  }

  ~MyType()
  {
    std::cout << "MyType::~MyType()\n" << std::flush;
  }

  std::string const &get() const
  {
    std::cout << "MyType::get()\n" << std::flush;
    return m_s;
  }

private:

  std::string m_s;
};
