#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class CStringTypeInfo(TypeInfo):

  def __init__(self, jinjenv, undq_cpp_type_expr):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base = "String",
      edk_name = "Fabric::EDK::KL::String",
      lib_expr = undq_cpp_type_expr,
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["edk_to_lib"] = "types/builtin/c_string/conv"
    tds["conv"]["lib_to_edk"] = "types/builtin/c_string/conv"
    return tds

class CStringSelector(Selector):

  direct_cpp_type_expr = PointerTo(Const(Char()))
  const_reference_cpp_type_expr = ReferenceTo(Const(PointerTo(Const(Char()))))

  def __init__(self, jinjenv):
    Selector.__init__(self, jinjenv)

  def get_desc(self):
    return "CString"
    
  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    if cpp_type_expr == self.direct_cpp_type_expr:
      return DirQualTypeInfo(
        dir_qual.direct,
        CStringTypeInfo(self.jinjenv, cpp_type_expr.make_unqualified())
        )
    if cpp_type_expr == self.const_reference_cpp_type_expr:
      return DirQualTypeInfo(
        dir_qual.const_reference,
        CStringTypeInfo(self.jinjenv, cpp_type_expr.pointee.make_unqualified())
        )
