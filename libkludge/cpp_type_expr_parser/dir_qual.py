#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
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
  def is_const_ref(self):
    return self.direction == directions.Reference and qualifiers.is_const(self.qualifier)
  
  @property
  def is_const_ptr(self):
    return self.direction == directions.Pointer and qualifiers.is_const(self.qualifier)

  @property
  def is_mutable_ref(self):
    return self.direction == directions.Reference and qualifiers.is_mutable(self.qualifier)
  
  @property
  def is_mutable_ptr(self):
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
    if self.is_const_ref:
      return "const_ref"
    if self.is_const_ptr:
      return "const_ptr"
    if self.is_mutable_ref:
      return "mutable_ref"
    if self.is_mutable_ptr:
      return "mutable_ptr"

  def __str__(self):
    return self.get_desc()

direct = DirQual(directions.Direct, qualifiers.Unqualified)
const_ref = DirQual(directions.Reference, qualifiers.Const)
const_ptr = DirQual(directions.Pointer, qualifiers.Const)
mutable_ref = DirQual(directions.Reference, qualifiers.Unqualified)
mutable_ptr = DirQual(directions.Pointer, qualifiers.Unqualified)
