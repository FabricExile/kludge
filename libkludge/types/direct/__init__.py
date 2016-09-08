#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class DirectTypeInfo(TypeInfo):

  def __init__(
    self,
    jinjenv,
    kl_global_name,

    undq_cpp_type_expr,
    kl_base_name=None,
    kl_suffix=None,
    ):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base = kl_global_name,
      lib_expr = undq_cpp_type_expr,
      )

  def build_codec_lookup_rules(self):
    rules = TypeInfo.build_codec_lookup_rules(self)
    rules["conv"]["*"] = "types/builtin/direct/conv"
    rules["result"]["*"] = "types/builtin/direct/result"
    rules["repr"]["*"] = "types/builtin/direct/repr"
    return rules

class DirectSelector(Selector):

  def __init__(
    self,
    ext,
    kl_global_name,
    cpp_type_expr,
    ):
    Selector.__init__(self, ext)
    self.kl_global_name = kl_global_name
    self.cpp_type_expr = cpp_type_expr

  def get_desc(self):
    return "Direct:%s" % str(self.cpp_type_expr)

  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    undq_cpp_type_expr, dq = cpp_type_expr.get_undq()
    if undq_cpp_type_expr == self.cpp_type_expr:
      return DirQualTypeInfo(
        dq,
        DirectTypeInfo(
          self.jinjenv,
          self.kl_global_name,
          undq_cpp_type_expr,
          )
        )
