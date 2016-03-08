#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

Unqualified = 0
Const = 1
Volatile = 2
ConstVolatile = 3

def is_const(qualifier):
  return qualifier == Const or qualifier == ConstVolatile

def is_mutable(qualifier):
  return not is_const(qualifier)

def make_const(qualifier):
  if qualifier == Unqualified or qualifier == Const:
    return Const
  else:
    return ConstVolatile

def is_volatile(qualifier):
  return qualifier == Volatile or qualifier == ConstVolatile

def make_volatile(qualifier):
  if qualifier == Unqualified or qualifier == Volatile:
    return Volatile
  else:
    return ConstVolatile
