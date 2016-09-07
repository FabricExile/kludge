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
      edk_name = "Fabric::EDK::KL::VariableArray< " + element_dqti.type_info.edk.name + " >",
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
    undq_cpp_type_expr, dq = cpp_type_expr.get_undq()
    if isinstance(undq_cpp_type_expr, Named) \
      and len(undq_cpp_type_expr.components) == 2 \
      and undq_cpp_type_expr.components[0] == Simple("std") \
      and isinstance(undq_cpp_type_expr.components[1], Template) \
      and undq_cpp_type_expr.components[1].name == "vector" \
      and len(undq_cpp_type_expr.components[1].params) == 1:
      element_dqti = type_mgr.get_dqti(undq_cpp_type_expr.components[1].params[0])
      return DirQualTypeInfo(
        dq,
        StdVectorTypeInfo(
          self.jinjenv,
          undq_cpp_type_expr,
          element_dqti,
          )
        )
