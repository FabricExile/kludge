#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class WrappedTypeInfo(TypeInfo):

  can_in_place = True

  def __init__(
    self,
    jinjenv,
    kl_type_name,
    nested_name,
    undq_cpp_type_expr,
    is_abstract,
    no_copy_constructor,
    ):
    TypeInfo.__init__(
      self,
      jinjenv,
      nested_name = nested_name,
      lib_expr = undq_cpp_type_expr,
      kl_name_base = kl_type_name,
      kl_name_suffix = '',
      )
    self.lib.is_abstract = is_abstract
    self.lib.no_copy_constructor = no_copy_constructor

  def build_codec_lookup_rules(self):
    rules = TypeInfo.build_codec_lookup_rules(self)
    rules["conv"]["*"] = "types/builtin/wrapped/conv"
    rules["result"]["indirect_init_edk"] = "types/builtin/wrapped/result"
    rules["result"]["decl_and_assign_lib"] = "types/builtin/wrapped/result"
    rules["repr"]["new_begin"] = "types/builtin/wrapped/repr"
    rules["repr"]["new_end"] = "types/builtin/wrapped/repr"
    rules["repr"]["ref"] = "types/builtin/wrapped/repr"
    rules["repr"]["member_ref"] = "types/builtin/wrapped/repr"
    return rules

class WrappedSelector(Selector):

  def __init__(
    self,
    jinjenv,
    kl_type_name,
    nested_name,
    cpp_type_expr,
    is_abstract,
    no_copy_constructor,
    ):
    Selector.__init__(self, jinjenv)
    self.kl_type_name = kl_type_name
    self.nested_name = nested_name
    self.cpp_type_expr = cpp_type_expr
    self.is_abstract = is_abstract
    self.no_copy_constructor = no_copy_constructor

  def get_desc(self):
    return "Wrapped:%s" % str(self.nested_name)

  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    if cpp_type_expr == self.cpp_type_expr:
      return DirQualTypeInfo(
        dir_qual.direct,
        WrappedTypeInfo(
          self.jinjenv,
          self.kl_type_name,
          self.nested_name,
          self.cpp_type_expr,
          self.is_abstract,
          self.no_copy_constructor,
          )
        )
