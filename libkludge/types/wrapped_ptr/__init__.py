#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class WrappedPtrTypeInfo(TypeInfo):

  can_in_place = True

  def __init__(self, jinjenv, nested_name, undq_cpp_type_expr, is_abstract, no_copy_constructor):
    TypeInfo.__init__(
      self,
      jinjenv,
      nested_name = nested_name,
      lib_expr = undq_cpp_type_expr,
      )
    self.lib.is_abstract = is_abstract
    self.lib.no_copy_constructor = no_copy_constructor

  def build_codec_lookup_rules(self):
    rules = TypeInfo.build_codec_lookup_rules(self)
    rules["conv"]["*"] = "types/builtin/wrapped_ptr/conv"
    rules["result"]["indirect_init_edk"] = "types/builtin/wrapped_ptr/result"
    return rules

class WrappedPtrSelector(Selector):

  def __init__(self, jinjenv, nested_name, cpp_type_expr, is_abstract, no_copy_constructor):
    Selector.__init__(self, jinjenv)
    self.nested_name = nested_name
    self.cpp_type_name = str(cpp_type_expr)
    self.is_abstract = is_abstract
    self.no_copy_constructor = no_copy_constructor

  def get_desc(self):
    return "WrappedPtr:%s" % str(self.nested_name)

  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    if (isinstance(cpp_type_expr, Named) or isinstance(cpp_type_expr, Template))\
      and str(cpp_type_expr) == self.cpp_type_name:
      return DirQualTypeInfo(
        dir_qual.direct,
        WrappedPtrTypeInfo(
          self.jinjenv,
          self.nested_name,
          cpp_type_expr.make_unqualified(),
          self.is_abstract,
          self.no_copy_constructor,
          )
        )

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
      if str(undq_cpp_type_expr) == self.cpp_type_name:
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
          WrappedPtrTypeInfo(
            self.jinjenv,
            self.nested_name,
            cpp_type_expr.pointee.make_unqualified(),
            self.is_abstract,
            self.no_copy_constructor,
            )
          )

