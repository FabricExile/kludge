from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.cpp_type_expr_parser import dir_qual
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class SimpleTypeInfo(TypeInfo):

  can_in_place = True

  def __init__(self, jinjenv, type_name_kl, undq_cpp_type_expr):
    TypeInfo.__init__(
      self,
      jinjenv,
      nested_name = [type_name_kl],
      lib_expr = undq_cpp_type_expr,
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "protocols/conv/builtin/none"
    tds["result"]["*"] = "protocols/result/builtin/direct"
    return tds

class SimpleSelector(Selector):

  boolean_type_info_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeInfo(jinjenv, "Boolean", undq_cpp_type_expr)
  sint8_type_info_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeInfo(jinjenv, "SInt8", undq_cpp_type_expr)
  uint8_type_info_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeInfo(jinjenv, "UInt8", undq_cpp_type_expr)
  sint16_type_info_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeInfo(jinjenv, "SInt16", undq_cpp_type_expr)
  uint16_type_info_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeInfo(jinjenv, "UInt16", undq_cpp_type_expr)
  sint32_type_info_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeInfo(jinjenv, "SInt32", undq_cpp_type_expr)
  uint32_type_info_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeInfo(jinjenv, "UInt32", undq_cpp_type_expr)
  sint64_type_info_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeInfo(jinjenv, "SInt64", undq_cpp_type_expr)
  uint64_type_info_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeInfo(jinjenv, "UInt64", undq_cpp_type_expr)
  float32_type_info_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeInfo(jinjenv, "Float32", undq_cpp_type_expr)
  float64_type_info_gen = lambda jinjenv, undq_cpp_type_expr: \
    SimpleTypeInfo(jinjenv, "Float64", undq_cpp_type_expr)

  type_name_lib_undq_to_simple_type_info_gen = {
    "bool": boolean_type_info_gen,
    "char": sint8_type_info_gen,
    "int8_t": sint8_type_info_gen,
    "unsigned char": uint8_type_info_gen,
    "uint8_t": uint8_type_info_gen,
    "short": sint16_type_info_gen,
    "int16_t": sint16_type_info_gen,
    "unsigned short": uint16_type_info_gen,
    "uint16_t": uint16_type_info_gen,
    "int": sint32_type_info_gen,
    "int32_t": sint32_type_info_gen,
    "unsigned int": uint32_type_info_gen,
    "uint32_t": uint32_type_info_gen,
    "long long": sint64_type_info_gen,
    "int64_t": sint64_type_info_gen,
    "unsigned long long": uint64_type_info_gen,
    "uint64_t": uint64_type_info_gen,
    "size_t": uint64_type_info_gen,
    "float": float32_type_info_gen,
    "double": float64_type_info_gen,
    #######################################################################
    # Warning: Linux + OS X ONLY
    # On Windows, these are 64-bit.  Not sure what to do about this.
    "long": sint32_type_info_gen,           
    "unsigned long": uint32_type_info_gen,
    #######################################################################
    }

  def __init__(self, jinjenv):
    Selector.__init__(self, jinjenv)

  def get_desc(self):
    return "Simple"
  
  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    if isinstance(cpp_type_expr, Direct):
      undq_cpp_type_expr = cpp_type_expr.make_unqualified()
      simple_type_info_gen = self.type_name_lib_undq_to_simple_type_info_gen.get(undq_cpp_type_expr.get_desc())
      if simple_type_info_gen:
        return DirQualTypeInfo(
          dir_qual.direct,
          simple_type_info_gen(self.jinjenv, undq_cpp_type_expr)
          )
    if isinstance(cpp_type_expr, PointerTo) \
      and isinstance(cpp_type_expr.pointee, Direct):
      undq_cpp_type_expr = cpp_type_expr.pointee.make_unqualified()
      simple_type_info_gen = self.type_name_lib_undq_to_simple_type_info_gen.get(undq_cpp_type_expr.get_desc())
      if simple_type_info_gen:
        if cpp_type_expr.pointee.is_const:
          dq = dir_qual.const_pointer
        else:
          dq = dir_qual.mutable_pointer
        return DirQualTypeInfo(
          dq,
          simple_type_info_gen(self.jinjenv, undq_cpp_type_expr)
          )
    if isinstance(cpp_type_expr, ReferenceTo) \
      and isinstance(cpp_type_expr.pointee, Direct):
      undq_cpp_type_expr = cpp_type_expr.pointee.make_unqualified()
      simple_type_info_gen = self.type_name_lib_undq_to_simple_type_info_gen.get(undq_cpp_type_expr.get_desc())
      if simple_type_info_gen:
        if cpp_type_expr.pointee.is_const:
          dq = dir_qual.const_reference
        else:
          dq = dir_qual.mutable_reference
        return DirQualTypeInfo(
          dq,
          simple_type_info_gen(self.jinjenv, undq_cpp_type_expr)
          )
