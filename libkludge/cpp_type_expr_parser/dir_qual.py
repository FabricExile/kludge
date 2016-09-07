#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import directions, qualifiers

class DirQual:

  def __init__(self, direction, qualifier):
    self.direction = direction
    self.qualifier = qualifier

  @property
  def is_direct(self):
    return self.direction == directions.Direct
  
  @property
  def is_const(self):
    return qualifiers.is_const(self.qualifier)
  
  @property
  def is_const_reference(self):
    return self.direction == directions.Reference and qualifiers.is_const(self.qualifier)
  
  @property
  def is_const_pointer(self):
    return self.direction == directions.Pointer and qualifiers.is_const(self.qualifier)
  
  @property
  def is_mutable_reference(self):
    return self.direction == directions.Reference and qualifiers.is_mutable(self.qualifier)
  
  @property
  def is_mutable_pointer(self):
    return self.direction == directions.Pointer and qualifiers.is_mutable(self.qualifier)
  
  @property
  def is_const_indirect(self):
    return self.direction != directions.Direct and qualifiers.is_const(self.qualifier)
  
  @property
  def is_mutable_indirect(self):
    return self.direction != directions.Direct and qualifiers.is_mutable(self.qualifier)
  
  @property
  def is_pointer(self):
    return self.direction == directions.Pointer
  
  @property
  def is_reference(self):
    return self.direction == directions.Reference

  def get_desc(self):
    if self.is_direct:
      return "direct"
    if self.is_const_reference:
      return "const_reference"
    if self.is_const_pointer:
      return "const_pointer"
    if self.is_mutable_reference:
      return "mutable_reference"
    if self.is_mutable_pointer:
      return "mutable_pointer"

direct = DirQual(directions.Direct, qualifiers.Unqualified)
const_reference = DirQual(directions.Reference, qualifiers.Const)
const_pointer = DirQual(directions.Pointer, qualifiers.Const)
mutable_reference = DirQual(directions.Reference, qualifiers.Unqualified)
mutable_pointer = DirQual(directions.Pointer, qualifiers.Unqualified)
