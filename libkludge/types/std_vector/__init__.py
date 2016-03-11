#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class StdVectorTypeInfo(TypeInfo):

  def __init__(self, jinjenv, undq_cpp_type_expr, element_dqti):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base = element_dqti.type_info.kl.name.base,
      kl_name_suffix = "[]" + element_dqti.type_info.kl.name.suffix,
      edk_name_toplevel = "::Fabric::EDK::KL::VariableArray< " + element_dqti.type_info.edk.name.toplevel + " >",
      lib_expr = undq_cpp_type_expr,
      child_dqtis = [element_dqti]
      )

  def build_codec_lookup_rules(self):
    rules = TypeInfo.build_codec_lookup_rules(self)
    rules["conv"]["*"] = "types/builtin/std_vector/conv"
    return rules

class StdVectorSelector(Selector):

  def __init__(self, jinjenv):
    Selector.__init__(self, jinjenv)

  def get_desc(self):
    return "StdVector"

  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    if isinstance(cpp_type_expr, Template) \
      and cpp_type_expr.name == "std::vector" \
      and len(cpp_type_expr.params) == 1:
      element_dqti = type_mgr.get_dqti(cpp_type_expr.params[0])
      return DirQualTypeInfo(
        dir_qual.direct,
        StdVectorTypeInfo(
          self.jinjenv,
          cpp_type_expr.make_unqualified(),
          element_dqti,
          )
        )
    if isinstance(cpp_type_expr, ReferenceTo) \
      and isinstance(cpp_type_expr.pointee, Template) \
      and cpp_type_expr.pointee.is_const \
      and cpp_type_expr.pointee.name == "std::vector" \
      and len(cpp_type_expr.pointee.params) == 1:
      element_dqti = type_mgr.get_dqti(cpp_type_expr.pointee.params[0])
      return DirQualTypeInfo(
        dir_qual.const_reference,
        StdVectorTypeInfo(
          self.jinjenv,
          cpp_type_expr.pointee.make_unqualified(),
          element_dqti,
          )
        )
