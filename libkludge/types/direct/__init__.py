#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class DirectTypeInfo(TypeInfo):

  can_in_place = True

  def __init__(
    self,
    jinjenv,
    kl_type_name,
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
      kl_name_base = kl_type_name,
      kl_name_suffix = '',
      )
    self.lib.is_abstract = is_abstract
    self.lib.no_copy_constructor = no_copy_constructor

  def build_codec_lookup_rules(self):
    rules = TypeInfo.build_codec_lookup_rules(self)
    rules["conv"]["*"] = "types/builtin/cpp_ptr/conv"
    rules["result"]["indirect_init_edk"] = "types/builtin/cpp_ptr/result"
    return rules

class DirectSelector(Selector):

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
    return "Direct:%s" % str(self.nested_name)

  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    if cpp_type_expr == self.cpp_type_expr:
      result = DirQualTypeInfo(
        dir_qual.direct,
        DirectTypeInfo(
          self.jinjenv,
          self.kl_type_name,
          self.nested_name,
          cpp_type_expr.make_unqualified(),
          self.is_abstract,
          self.no_copy_constructor,
          )
        )
      return result

    is_reference = isinstance(cpp_type_expr, ReferenceTo)
    is_pointer = isinstance(cpp_type_expr, PointerTo)

    # FIXME special case, e.g. "Class * &" we drop to just "Class *"
    if is_reference and isinstance(cpp_type_expr.pointee, PointerTo):
      cpp_type_expr = cpp_type_expr.pointee
      is_pointer = True
      is_reference = False

    if (is_pointer or is_reference) \
      and (isinstance(cpp_type_expr.pointee, Named) or \
        isinstance(cpp_type_expr.pointee, Template)):
      undq_cpp_type_expr, _ = cpp_type_expr.pointee.get_undq_type_expr_and_dq()
      if undq_cpp_type_expr == self.cpp_type_expr:
        if is_pointer:
          if cpp_type_expr.pointee.is_const:
            dq = dir_qual.const_pointer
          else:
            dq = dir_qual.mutable_pointer
        else:
          if cpp_type_expr.pointee.is_const:
            dq = dir_qual.const_reference
          else:
            dq = dir_qual.mutable_reference
        return DirQualTypeInfo(
          dq,
          DirectTypeInfo(
            self.jinjenv,
            self.kl_type_name,
            self.nested_name,
            cpp_type_expr.pointee.make_unqualified(),
            self.is_abstract,
            self.no_copy_constructor,
            )
          )
