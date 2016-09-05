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
      kl_name_base = "String",
      edk_name = "Fabric::EDK::KL::String",
      lib_expr = undq_cpp_type_expr,
      )

  def build_codec_lookup_rules(self):
    rules = TypeInfo.build_codec_lookup_rules(self)
    rules["conv"]["edk_to_lib"] = "types/builtin/std_string/conv"
    rules["conv"]["lib_to_edk"] = "types/builtin/std_string/conv"
    return rules

class StdStringSelector(Selector):

  def __init__(self, jinjenv):
    Selector.__init__(self, jinjenv)
    self.cpp_type_expr = Named([
      Simple('std'),
      Simple('string'),
      ])

  def get_desc(self):
    return "StdString"

  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    undq_cpp_type_expr, dq = cpp_type_expr.get_undq_type_expr_and_dq()
    if undq_cpp_type_expr == self.cpp_type_expr:
      return DirQualTypeInfo(
        dq,
        StdStringTypeInfo(
          self.jinjenv,
          undq_cpp_type_expr
          )
        )
