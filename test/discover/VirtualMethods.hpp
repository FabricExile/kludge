//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

class AbstractClass
{
public:
  virtual const char * GetName() = 0;
};

class ParentClass : public AbstractClass
{
public:
  virtual const char * GetName() { return "ParentClass"; }
};

class ChildClass : public ParentClass
{
public:
  virtual const char * GetName() { return "ChildClass"; }
};
