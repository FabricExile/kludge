from libkludge.type_codec import TypeCodec
from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_codec import DirQualTypeCodec
from libkludge.cpp_type_expr_parser import *

class CStringTypeCodec(TypeCodec):

  def __init__(self, jinjenv, undq_cpp_type_expr):
    TypeCodec.__init__(
      self,
      jinjenv,
      TypeInfo(
        name = "String",
        lib_expr = undq_cpp_type_expr,
        )
      )

  def build_type_dir_spec(self):
    tds = TypeCodec.build_type_dir_spec(self)
    tds["conv"]["edk_to_lib"] = "types/builtin/c_string/conv"
    tds["conv"]["lib_to_edk"] = "types/builtin/c_string/conv"
    return tds

class CStringSelector(Selector):

  direct_cpp_type_expr = PointerTo(Const(Char()))
  const_reference_cpp_type_expr = ReferenceTo(Const(PointerTo(Const(Char()))))

  def __init__(self, jinjenv):
    Selector.__init__(self, jinjenv)

  def maybe_create_dqtc(self, type_mgr, cpp_type_expr):
    if cpp_type_expr == self.direct_cpp_type_expr:
      return DirQualTypeCodec(
        dir_qual.direct,
        CStringTypeCodec(self.jinjenv, cpp_type_expr.make_unqualified())
        )
    if cpp_type_expr == self.const_reference_cpp_type_expr:
      return DirQualTypeCodec(
        dir_qual.const_reference,
        CStringTypeCodec(self.jinjenv, cpp_type_expr.pointee.make_unqualified())
        )
