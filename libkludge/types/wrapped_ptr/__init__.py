#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class WrappedPtrTypeInfo(TypeInfo):

  can_in_place = True

  def __init__(self, jinjenv, nested_name, undq_cpp_type_expr):
    TypeInfo.__init__(
      self,
      jinjenv,
      nested_name = nested_name,
      lib_expr = undq_cpp_type_expr,
      )

  def build_codec_lookup_rules(self):
    rules = TypeInfo.build_codec_lookup_rules(self)
    rules["conv"]["*"] = "types/builtin/wrapped_ptr/conv"
    rules["result"]["indirect_init_edk"] = "types/builtin/wrapped_ptr/result"
    return rules

class WrappedPtrSelector(Selector):

  def __init__(self, jinjenv, nested_name):
    Selector.__init__(self, jinjenv)
    self.nested_name = nested_name
    self.cpp_type_name = "::".join(nested_name)

  def get_desc(self):
    return "WrappedPtr:%s" % str(self.nested_name)

  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    if isinstance(cpp_type_expr, Named) \
      and cpp_type_expr.name == self.cpp_type_name:
      return DirQualTypeInfo(
        dir_qual.direct,
        WrappedPtrTypeInfo(
          self.jinjenv,
          self.nested_name,
          cpp_type_expr.make_unqualified()
          )
        )
    if isinstance(cpp_type_expr, ReferenceTo) \
      and isinstance(cpp_type_expr.pointee, Named) \
      and cpp_type_expr.pointee.is_const \
      and cpp_type_expr.pointee.name == self.cpp_type_name:
      return DirQualTypeInfo(
        dir_qual.const_reference,
        WrappedPtrTypeInfo(
          self.jinjenv,
          self.nested_name,
          cpp_type_expr.pointee.make_unqualified()
          )
        )
