from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.cpp_type_expr_parser import dir_qual
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *

class SimpleDirectTypeInfo(TypeInfo):

  def __init__(self, jinjenv, type_name_kl, undq_cpp_type_expr):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base = type_name_kl,
      edk_name = "Fabric::EDK::KL::" + type_name_kl,
      lib_expr = undq_cpp_type_expr,
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "protocols/conv/builtin/none"
    tds["result"]["*"] = "protocols/result/builtin/direct"
    tds["repr"]["new_begin"] = "types/builtin/simple_direct/repr"
    tds["repr"]["new_end"] = "types/builtin/simple_direct/repr"
    return tds

class SimpleDirectSelector(Selector):

  boolean_type_info_gen = lambda jinjenv: \
    SimpleDirectTypeInfo(jinjenv, "Boolean", Bool())
  sint8_type_info_gen = lambda jinjenv: \
    SimpleDirectTypeInfo(jinjenv, "SInt8", Named([Simple("int8_t")]))
  uint8_type_info_gen = lambda jinjenv: \
    SimpleDirectTypeInfo(jinjenv, "UInt8", Named([Simple("uint8_t")]))
  sint16_type_info_gen = lambda jinjenv: \
    SimpleDirectTypeInfo(jinjenv, "SInt16", Named([Simple("int16_t")]))
  uint16_type_info_gen = lambda jinjenv: \
    SimpleDirectTypeInfo(jinjenv, "UInt16", Named([Simple("uint16_t")]))
  sint32_type_info_gen = lambda jinjenv: \
    SimpleDirectTypeInfo(jinjenv, "SInt32", Named([Simple("int32_t")]))
  uint32_type_info_gen = lambda jinjenv: \
    SimpleDirectTypeInfo(jinjenv, "UInt32", Named([Simple("uint32_t")]))
  sint64_type_info_gen = lambda jinjenv: \
    SimpleDirectTypeInfo(jinjenv, "SInt64", Named([Simple("int64_t")]))
  uint64_type_info_gen = lambda jinjenv: \
    SimpleDirectTypeInfo(jinjenv, "UInt64", Named([Simple("uint64_t")]))
  float32_type_info_gen = lambda jinjenv: \
    SimpleDirectTypeInfo(jinjenv, "Float32", Float())
  float64_type_info_gen = lambda jinjenv: \
    SimpleDirectTypeInfo(jinjenv, "Float64", Double())

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
    "ptrdiff_t": uint64_type_info_gen,
    "float": float32_type_info_gen,
    "double": float64_type_info_gen,
    #######################################################################
    # Warning: Linux + OS X ONLY
    # On Windows, these are 64-bit.  Not sure what to do about this.
    "long": sint32_type_info_gen,           
    "unsigned long": uint32_type_info_gen,
    #######################################################################
    }

  def __init__(self, ext):
    Selector.__init__(self, ext)

  def get_desc(self):
    return "SimpleDirect"
  
  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    undq_cpp_type_expr, dq = cpp_type_expr.get_undq()
    simple_type_info_gen = self.type_name_lib_undq_to_simple_type_info_gen.get(undq_cpp_type_expr.get_desc())
    if simple_type_info_gen:
      return DirQualTypeInfo(
        dq,
        simple_type_info_gen(self.jinjenv)
        )
