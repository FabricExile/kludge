from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.cpp_type_expr_parser import dir_qual
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *
from libkludge.generate.builtin_decl import BuiltinDecl

class SimpleTypeInfo(TypeInfo):

  def __init__(self, jinjenv, type_name_kl, type_name_edk, undq_cpp_type_expr):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base = type_name_kl,
      edk_name = "Fabric::EDK::KL::" + type_name_edk,
      lib_expr = undq_cpp_type_expr,
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "protocols/conv/builtin/none"
    tds["result"]["*"] = "protocols/result/builtin/direct"
    tds["repr"]["new_begin"] = "types/builtin/simple/repr"
    tds["repr"]["new_end"] = "types/builtin/simple/repr"
    return tds

class SimpleBuiltinDecl(BuiltinDecl):

  def __init__(self, ext, type_info):
    BuiltinDecl.__init__(
      self,
      ext.root_namespace,
      desc="Simple %s" % type_info,
      template_path="types/builtin/simple/simple",
      test_name="Simple_%s" % type_info.kl.name,
      )
    self.type_info = type_info

class SimpleSelector(Selector):

  cpp_type_name_to_kl_type_name = {
    "bool": 'CxxBool',
    "char": 'CxxChar',
    "int8_t": 'CxxChar',
    "unsigned char": 'CxxUChar',
    "uint8_t": 'CxxUChar',
    "short": 'CxxShort',
    "int16_t": 'CxxShort',
    "unsigned short": 'CxxUShort',
    "uint16_t": 'CxxUShort',
    "int": 'CxxInt',
    "int32_t": 'CxxInt',
    "unsigned int": 'CxxUInt',
    "uint32_t": 'CxxUInt',
    "long long": 'CxxLongLong',
    "int64_t": 'CxxLongLong',
    "unsigned long long": 'CxxULongLong',
    "uint64_t": 'CxxULongLong',
    "size_t": 'CxxULongLong',
    "ptrdiff_t": 'CxxULongLong',
    "float": 'CxxFloat',
    "double": 'CxxDouble',
    #######################################################################
    # Warning: Linux + OS X ONLY
    # On Windows, these are 64-bit.  Not sure what to do about this.
    "long": 'CxxInt',           
    "unsigned long": 'CxxUInt',
    #######################################################################
    }

  kl_type_name_to_edk_type_name_and_cpp_type_expr = {
    'CxxBool': ("Boolean", Bool()),
    'CxxChar': ("SInt8", Named([Simple("int8_t")])),
    'CxxUChar': ("UInt8", Named([Simple("uint8_t")])),
    'CxxShort': ("SInt16", Named([Simple("int16_t")])),
    'CxxUShort': ("UInt16", Named([Simple("uint16_t")])),
    'CxxInt': ("SInt32", Named([Simple("int32_t")])),
    'CxxUInt': ("UInt32", Named([Simple("uint32_t")])),
    'CxxLongLong': ("SInt64", Named([Simple("int64_t")])),
    'CxxULongLong': ("UInt64", Named([Simple("uint64_t")])),
    'CxxFloat': ("Float32", Float()),
    'CxxDouble': ("Float64", Double()),
    }

  def __init__(self, ext):
    Selector.__init__(self, ext)
    self.kl_type_name_to_existing_ti = {}

  def get_desc(self):
    return "Simple"
  
  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    undq_cpp_type_expr, dq = cpp_type_expr.get_undq()
    kl_type_name = self.cpp_type_name_to_kl_type_name.get(str(undq_cpp_type_expr))
    if kl_type_name:
      ti = self.kl_type_name_to_existing_ti.get(kl_type_name)
      if not ti:
        edk_type_name, undq_cpp_type_expr = self.kl_type_name_to_edk_type_name_and_cpp_type_expr[kl_type_name]
        ti = SimpleTypeInfo(self.jinjenv, kl_type_name, edk_type_name, undq_cpp_type_expr)
        self.kl_type_name_to_existing_ti.setdefault(kl_type_name, ti)
        if dq.is_direct:
          self.ext.decls.append(SimpleBuiltinDecl(self.ext, ti))
      return DirQualTypeInfo(dq, ti)
