//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

#include <iostream>
#include <sstream>
#include <string>
#include <vector>

class MyClass
{
public:

  MyClass(const char * caption)
  : m_caption(caption)
  {}

  const char * caption() const { return m_caption.c_str(); }

  void setCaption(const char * caption)
  {
    m_caption = caption;
  }

  static const MyClass * cast(const MyClass * element)
  {
    return element;
  }

  static MyClass * cast(MyClass * element)
  {
    return element;
  }

private:
  std::string m_caption;
};
