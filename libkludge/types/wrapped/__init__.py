#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class WrappedTypeInfo(TypeInfo):

  def __init__(
    self,
    jinjenv,
    kl_type_name,
    undq_cpp_type_expr,
    ):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base = kl_type_name,
      lib_expr = undq_cpp_type_expr,
      )

  def build_codec_lookup_rules(self):
    rules = TypeInfo.build_codec_lookup_rules(self)
    rules["conv"]["*"] = "types/builtin/wrapped/conv"
    rules["result"]["indirect_init_edk"] = "types/builtin/wrapped/result"
    rules["result"]["decl_and_assign_lib_begin"] = "types/builtin/wrapped/result"
    rules["result"]["decl_and_assign_lib_end"] = "types/builtin/wrapped/result"
    rules["repr"]["*"] = "types/builtin/wrapped/repr"
    return rules

class WrappedSelector(Selector):

  def __init__(
    self,
    jinjenv,
    kl_type_name,
    cpp_type_expr,
    ):
    Selector.__init__(self, jinjenv)
    self.kl_type_name = kl_type_name
    self.cpp_type_expr = cpp_type_expr

  def get_desc(self):
    return "Wrapped:%s" % str(self.cpp_type_expr)

  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    undq_cpp_type_expr, dq = cpp_type_expr.get_undq()
    if undq_cpp_type_expr == self.cpp_type_expr:
      return DirQualTypeInfo(
        dq,
        WrappedTypeInfo(
          self.jinjenv,
          self.kl_type_name,
          self.cpp_type_expr,
          )
        )
