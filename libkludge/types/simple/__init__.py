from libkludge.type_codec import TypeCodec
from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.cpp_type_expr_parser import dir_qual
from libkludge.dir_qual_type_codec import DirQualTypeCodec
from libkludge.cpp_type_expr_parser import *

class SimpleTypeCodec(TypeCodec):

  is_in_place = True

  def __init__(self, jinjenv, type_name_kl, undq_cpp_type_expr):
    TypeCodec.__init__(
      self,
      jinjenv,
      TypeInfo(
        name = type_name_kl,
        lib_expr = undq_cpp_type_expr,
        )
      )

  def build_type_dir_spec(self):
    tds = TypeCodec.build_type_dir_spec(self)
    tds["conv"]["*"] = "protocols/conv/builtin/none"
    tds["result"]["*"] = "protocols/result/builtin/direct"
    return tds

class SimpleSelector(Selector):

  boolean_type_codec_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeCodec(jinjenv, "Boolean", undq_cpp_type_expr)
  sint8_type_codec_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeCodec(jinjenv, "SInt8", undq_cpp_type_expr)
  uint8_type_codec_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeCodec(jinjenv, "UInt8", undq_cpp_type_expr)
  sint16_type_codec_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeCodec(jinjenv, "SInt16", undq_cpp_type_expr)
  uint16_type_codec_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeCodec(jinjenv, "UInt16", undq_cpp_type_expr)
  sint32_type_codec_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeCodec(jinjenv, "SInt32", undq_cpp_type_expr)
  uint32_type_codec_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeCodec(jinjenv, "UInt32", undq_cpp_type_expr)
  sint64_type_codec_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeCodec(jinjenv, "SInt64", undq_cpp_type_expr)
  uint64_type_codec_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeCodec(jinjenv, "UInt64", undq_cpp_type_expr)
  float32_type_codec_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeCodec(jinjenv, "Float32", undq_cpp_type_expr)
  float64_type_codec_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeCodec(jinjenv, "Float64", undq_cpp_type_expr)

  type_name_lib_undq_to_simple_type_codec_gen = {
    "bool": boolean_type_codec_gen,
    "char": sint8_type_codec_gen,
    "int8_t": sint8_type_codec_gen,
    "unsigned char": uint8_type_codec_gen,
    "uint8_t": uint8_type_codec_gen,
    "short": sint16_type_codec_gen,
    "int16_t": sint16_type_codec_gen,
    "unsigned short": uint16_type_codec_gen,
    "uint16_t": uint16_type_codec_gen,
    "int": sint32_type_codec_gen,
    "int32_t": sint32_type_codec_gen,
    "unsigned int": uint32_type_codec_gen,
    "uint32_t": uint32_type_codec_gen,
    "long long": sint64_type_codec_gen,
    "int64_t": sint64_type_codec_gen,
    "unsigned long long": uint64_type_codec_gen,
    "uint64_t": uint64_type_codec_gen,
    "float": float32_type_codec_gen,
    "double": float64_type_codec_gen,
    #######################################################################
    # Warning: Linux + OS X ONLY
    # On Windows, these are 64-bit.  Not sure what to do about this.
    "long": sint32_type_codec_gen,           
    "unsigned long": uint32_type_codec_gen,
    #######################################################################
    }

  def __init__(self, jinjenv):
    Selector.__init__(self, jinjenv)

  def maybe_create_dqtc(self, type_mgr, cpp_type_expr):
    if isinstance(cpp_type_expr, Direct):
      undq_cpp_type_expr = cpp_type_expr.make_unqualified()
      simple_type_codec_gen = self.type_name_lib_undq_to_simple_type_codec_gen.get(undq_cpp_type_expr.get_desc())
      if simple_type_codec_gen:
        return DirQualTypeCodec(
          dir_qual.direct,
          simple_type_codec_gen(self.jinjenv, undq_cpp_type_expr)
          )
    if isinstance(cpp_type_expr, PointerTo) \
      and isinstance(cpp_type_expr.pointee, Direct):
      undq_cpp_type_expr = cpp_type_expr.pointee.make_unqualified()
      simple_type_codec_gen = self.type_name_lib_undq_to_simple_type_codec_gen.get(undq_cpp_type_expr.get_desc())
      if simple_type_codec_gen:
        if cpp_type_expr.pointee.is_const:
          dq = dir_qual.const_pointer
        else:
          dq = dir_qual.mutable_pointer
        return DirQualTypeCodec(
          dq,
          simple_type_codec_gen(self.jinjenv, undq_cpp_type_expr)
          )
    if isinstance(cpp_type_expr, ReferenceTo) \
      and isinstance(cpp_type_expr.pointee, Direct):
      undq_cpp_type_expr = cpp_type_expr.pointee.make_unqualified()
      simple_type_codec_gen = self.type_name_lib_undq_to_simple_type_codec_gen.get(undq_cpp_type_expr.get_desc())
      if simple_type_codec_gen:
        if cpp_type_expr.pointee.is_const:
          dq = dir_qual.const_reference
        else:
          dq = dir_qual.mutable_reference
        return DirQualTypeCodec(
          dq,
          simple_type_codec_gen(self.jinjenv, undq_cpp_type_expr)
          )
