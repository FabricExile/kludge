#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class WrappedPtrTypeInfo(TypeInfo):

  can_in_place = True

  def __init__(
    self,
    jinjenv,
    cpp_wrapper_name,
    nested_name,
    undq_cpp_type_expr,
    is_abstract,
    no_copy_constructor,
    kl_base_name=None,
    kl_suffix=None,
    ):
    TypeInfo.__init__(
      self,
      jinjenv,
      nested_name = nested_name,
      lib_expr = undq_cpp_type_expr,
      )
    self.lib.is_abstract = is_abstract
    self.lib.no_copy_constructor = no_copy_constructor
    self.cpp_wrapper_name = cpp_wrapper_name

  def build_codec_lookup_rules(self):
    rules = TypeInfo.build_codec_lookup_rules(self)
    rules["conv"]["*"] = "types/builtin/wrapped_ptr/conv"
    rules["result"]["indirect_init_edk"] = "types/builtin/wrapped_ptr/result"
    rules["result"]["decl_and_assign_lib"] = "types/builtin/wrapped_ptr/result"
    rules["repr"]["defn_edk"] = "types/builtin/wrapped_ptr/repr"
    rules["repr"]["ref"] = "types/builtin/wrapped_ptr/repr"
    rules["repr"]["member_ref"] = "types/builtin/wrapped_ptr/repr"
    rules["repr"]["new_begin"] = "types/builtin/wrapped_ptr/repr"
    rules["repr"]["new_end"] = "types/builtin/wrapped_ptr/repr"
    return rules

class WrappedPtrSelector(Selector):

  def __init__(
    self,
    jinjenv,
    cpp_wrapper_name,
    nested_name,
    cpp_type_expr,
    is_abstract,
    no_copy_constructor,
    ):
    Selector.__init__(self, jinjenv)
    self.cpp_wrapper_name = cpp_wrapper_name
    self.nested_name = nested_name
    self.cpp_type_expr = cpp_type_expr
    self.is_abstract = is_abstract
    self.no_copy_constructor = no_copy_constructor

  def get_desc(self):
    return "WrappedPtr:%s<%s>" % (self.cpp_wrapper_name, str(self.nested_name))

  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    if cpp_type_expr == self.cpp_type_expr:
      return DirQualTypeInfo(
        dir_qual.direct,
        WrappedPtrTypeInfo(
          self.jinjenv,
          self.cpp_wrapper_name,
          self.nested_name,
          self.cpp_type_expr.pointee,
          self.is_abstract,
          self.no_copy_constructor,
          )
        )
