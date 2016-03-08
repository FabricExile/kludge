#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_codec import TypeCodec
from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_codec import DirQualTypeCodec
from libkludge.cpp_type_expr_parser import *

class WrappedPtrTypeCodec(TypeCodec):

  is_in_place = True

  def __init__(self, jinjenv, name, undq_cpp_type_expr):
    TypeCodec.__init__(
      self,
      jinjenv,
      TypeInfo(
        name = name,
        lib_expr = undq_cpp_type_expr,
        )
      )

  def build_type_dir_spec(self):
    tds = TypeCodec.build_type_dir_spec(self)
    tds["conv"]["*"] = "types/builtin/wrapped_ptr/conv"
    tds["result"]["indirect_init_edk"] = "types/builtin/wrapped_ptr/result"
    return tds    

class WrappedPtrSelector(Selector):

  def __init__(self, jinjenv, cpp_type_name):
    Selector.__init__(self, jinjenv)
    self.cpp_type_name = cpp_type_name

  def maybe_create_dqtc(self, type_mgr, cpp_type_expr):
    if isinstance(cpp_type_expr, Named) \
      and cpp_type_expr.name == self.cpp_type_name:
      return DirQualTypeCodec(
        dir_qual.direct,
        WrappedPtrTypeCodec(
          self.jinjenv,
          self.cpp_type_name,
          cpp_type_expr.make_unqualified()
          )
        )
    if isinstance(cpp_type_expr, ReferenceTo) \
      and isinstance(cpp_type_expr.pointee, Named) \
      and cpp_type_expr.pointee.is_const \
      and cpp_type_expr.pointee.name == self.cpp_type_name:
      return DirQualTypeCodec(
        dir_qual.const_reference,
        WrappedPtrTypeCodec(
          self.jinjenv,
          self.cpp_type_name,
          cpp_type_expr.pointee.make_unqualified()
          )
        )
