#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class StdStringTypeInfo(TypeInfo):

  def __init__(self, jinjenv, undq_cpp_type_expr):
    TypeInfo.__init__(
      self,
      jinjenv,
      nested_name = ["String"],
      lib_expr = undq_cpp_type_expr,
      )

  def build_codec_lookup_rules(self):
    rules = TypeInfo.build_codec_lookup_rules(self)
    rules["conv"]["edk_to_lib"] = "types/builtin/std_string/conv"
    rules["conv"]["lib_to_edk"] = "types/builtin/std_string/conv"
    return rules

class StdStringSelector(Selector):

  cpp_type_names = [
    "std::string",
    ]

  def __init__(self, jinjenv):
    Selector.__init__(self, jinjenv)

  def get_desc(self):
    return "StdString"

  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    if isinstance(cpp_type_expr, Named) \
      and cpp_type_expr.name in self.cpp_type_names:
      return DirQualTypeInfo(
        dir_qual.direct,
        StdStringTypeInfo(
          self.jinjenv,
          cpp_type_expr.make_unqualified()
          )
        )
    if isinstance(cpp_type_expr, PointerTo) \
      and isinstance(cpp_type_expr.pointee, Named) \
      and cpp_type_expr.pointee.name in self.cpp_type_names:
      if cpp_type_expr.pointee.is_const:
        dq = dir_qual.const_pointer
      else:
        dq = dir_qual.mutable_pointer
      return DirQualTypeInfo(
        dq,
        StdStringTypeInfo(
          self.jinjenv,
          cpp_type_expr.pointee.make_unqualified()
          )
        )
    if isinstance(cpp_type_expr, ReferenceTo) \
      and isinstance(cpp_type_expr.pointee, Named) \
      and cpp_type_expr.pointee.name in self.cpp_type_names:
      if cpp_type_expr.pointee.is_const:
        dq = dir_qual.const_reference
      else:
        dq = dir_qual.mutable_reference
      return DirQualTypeInfo(
        dq,
        StdStringTypeInfo(
          self.jinjenv,
          cpp_type_expr.pointee.make_unqualified()
          )
        )
