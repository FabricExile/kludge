#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_codec import TypeCodec
from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_codec import DirQualTypeCodec
from libkludge.cpp_type_expr_parser import *

class StdStringTypeCodec(TypeCodec):

  def __init__(self, jinjenv, undq_cpp_type_expr):
    TypeCodec.__init__(
      self,
      jinjenv,
      TypeInfo(
        name = "String",
        lib_expr = undq_cpp_type_expr,
        )
      )

  def build_codec_lookup_rules(self):
    rules = TypeCodec.build_codec_lookup_rules(self)
    rules["conv"]["edk_to_lib"] = "types/builtin/std_string/conv"
    rules["conv"]["lib_to_edk"] = "types/builtin/std_string/conv"
    return rules

class StdStringSelector(Selector):

  def __init__(self, jinjenv):
    Selector.__init__(self, jinjenv)

  def maybe_create_dqtc(self, type_mgr, cpp_type_expr):
    if isinstance(cpp_type_expr, Named) \
      and cpp_type_expr.name == "std::string":
      return DirQualTypeCodec(
        dir_qual.direct,
        StdStringTypeCodec(
          self.jinjenv,
          cpp_type_expr.make_unqualified()
          )
        )
    if isinstance(cpp_type_expr, PointerTo) \
      and isinstance(cpp_type_expr.pointee, Named) \
      and cpp_type_expr.pointee.name == "std::string":
      if cpp_type_expr.pointee.is_const:
        dq = dir_qual.const_pointer
      else:
        dq = dir_qual.mutable_pointer
      return DirQualTypeCodec(
        dq,
        StdStringTypeCodec(
          self.jinjenv,
          cpp_type_expr.pointee.make_unqualified()
          )
        )
    if isinstance(cpp_type_expr, ReferenceTo) \
      and isinstance(cpp_type_expr.pointee, Named) \
      and cpp_type_expr.pointee.name == "std::string":
      if cpp_type_expr.pointee.is_const:
        dq = dir_qual.const_reference
      else:
        dq = dir_qual.mutable_reference
      return DirQualTypeCodec(
        dq,
        StdStringTypeCodec(
          self.jinjenv,
          cpp_type_expr.pointee.make_unqualified()
          )
        )
