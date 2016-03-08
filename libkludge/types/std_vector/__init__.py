#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_codec import TypeCodec
from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_codec import DirQualTypeCodec
from libkludge.cpp_type_expr_parser import *

class StdVectorTypeCodec(TypeCodec):

  def __init__(self, jinjenv, undq_cpp_type_expr, element_dqtc):
    TypeCodec.__init__(
      self,
      jinjenv,
      TypeInfo(
        kl_name_base = element_dqtc.type_info.kl.name.base,
        kl_name_suffix = "[]" + element_dqtc.type_info.kl.name.suffix,
        edk_name_toplevel = "::Fabric::EDK::KL::VariableArray< " + element_dqtc.type_info.edk.name.toplevel + " >",
        lib_expr = undq_cpp_type_expr,
        ),
      [element_dqtc]
      )

  def build_type_dir_spec(self):
    tds = TypeCodec.build_type_dir_spec(self)
    tds["conv"]["*"] = "types/builtin/std_vector/conv"
    return tds

class StdVectorSelector(Selector):

  def __init__(self, jinjenv):
    Selector.__init__(self, jinjenv)

  def maybe_create_dqtc(self, type_mgr, cpp_type_expr):
    if isinstance(cpp_type_expr, Template) \
      and cpp_type_expr.name == "std::vector" \
      and len(cpp_type_expr.params) == 1:
      element_dqtc = type_mgr.get_dqtc(cpp_type_expr.params[0])
      return DirQualTypeCodec(
        dir_qual.direct,
        StdVectorTypeCodec(
          self.jinjenv,
          cpp_type_expr.make_unqualified(),
          element_dqtc,
          )
        )
    if isinstance(cpp_type_expr, ReferenceTo) \
      and isinstance(cpp_type_expr.pointee, Template) \
      and cpp_type_expr.pointee.is_const \
      and cpp_type_expr.pointee.name == "std::vector" \
      and len(cpp_type_expr.pointee.params) == 1:
      element_dqtc = type_mgr.get_dqtc(cpp_type_expr.pointee.params[0])
      return DirQualTypeCodec(
        dir_qual.const_reference,
        StdVectorTypeCodec(
          self.jinjenv,
          cpp_type_expr.pointee.make_unqualified(),
          element_dqtc,
          )
        )
