#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.cpp_type_expr_parser import dir_qual
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *
from libkludge.generate.builtin_decl import BuiltinDecl

class SimpleDirectTypeInfo(TypeInfo):

  def __init__(self, jinjenv, kl_type_name, undq_cpp_type_expr):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base = kl_type_name,
      edk_name = "Fabric::EDK::KL::" + kl_type_name,
      lib_expr = undq_cpp_type_expr,
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "types/builtin/simple/direct/conv"
    tds["result"]["*"] = "protocols/result/builtin/direct"
    tds["repr"]["new_begin"] = "types/builtin/simple/repr"
    tds["repr"]["new_end"] = "types/builtin/simple/repr"
    return tds

class SimpleConstRefTypeInfo(TypeInfo):

  def __init__(self, jinjenv, kl_type_name, undq_cpp_type_expr):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base = kl_type_name + "ConstRef",
      edk_name = "Fabric_EDK_KL_" + kl_type_name + "ConstRef",
      lib_expr = ReferenceTo(Const(undq_cpp_type_expr)),
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "types/builtin/simple/ref/conv"
    tds["result"]["*"] = "protocols/result/builtin/indirect"
    tds["repr"]["new_begin"] = "types/builtin/simple/repr"
    tds["repr"]["new_end"] = "types/builtin/simple/repr"
    return tds

class SimpleMutableRefTypeInfo(TypeInfo):

  def __init__(self, jinjenv, kl_type_name, undq_cpp_type_expr):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base = kl_type_name + "Ref",
      edk_name = "Fabric_EDK_KL_" + kl_type_name + "MutableRef",
      lib_expr = ReferenceTo(undq_cpp_type_expr),
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "types/builtin/simple/ref/conv"
    tds["result"]["*"] = "protocols/result/builtin/indirect"
    tds["repr"]["new_begin"] = "types/builtin/simple/repr"
    tds["repr"]["new_end"] = "types/builtin/simple/repr"
    return tds

class SimpleConstPtrTypeInfo(TypeInfo):

  def __init__(self, jinjenv, kl_type_name, undq_cpp_type_expr):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base = kl_type_name + "ConstPtr",
      edk_name = "Fabric_EDK_KL_" + kl_type_name + "ConstPtr",
      lib_expr = PointerTo(Const(undq_cpp_type_expr)),
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "types/builtin/simple/ptr/conv"
    tds["result"]["*"] = "protocols/result/builtin/indirect"
    tds["repr"]["new_begin"] = "types/builtin/simple/repr"
    tds["repr"]["new_end"] = "types/builtin/simple/repr"
    return tds

class SimpleMutablePtrTypeInfo(TypeInfo):

  def __init__(self, jinjenv, kl_type_name, undq_cpp_type_expr):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base = kl_type_name + "Ptr",
      edk_name = "Fabric_EDK_KL_" + kl_type_name + "MutablePtr",
      lib_expr = PointerTo(undq_cpp_type_expr),
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "types/builtin/simple/ptr/conv"
    tds["result"]["*"] = "protocols/result/builtin/indirect"
    tds["repr"]["new_begin"] = "types/builtin/simple/repr"
    tds["repr"]["new_end"] = "types/builtin/simple/repr"
    return tds

class SimpleBuiltinDecl(BuiltinDecl):

  def __init__(self, ext, kl_type_name, cpp_type_expr):
    BuiltinDecl.__init__(
      self,
      ext.root_namespace,
      desc="Simple %s" % (kl_type_name),
      template_path="types/builtin/simple/simple",
      test_name="Simple_%s" % (kl_type_name),
      )
    self.kl_type_name = kl_type_name
    self.cpp_type_expr = cpp_type_expr

class SimpleSelector(Selector):

  cpp_type_name_to_kl_type_name = {
    "bool": 'Boolean',
    "char": 'SInt8',
    "int8_t": 'SInt8',
    "unsigned char": 'UInt8',
    "uint8_t": 'UInt8',
    "short": 'SInt16',
    "int16_t": 'SInt16',
    "unsigned short": 'UInt16',
    "uint16_t": 'UInt16',
    "int": 'SInt32',
    "int32_t": 'SInt32',
    "unsigned int": 'UInt32',
    "uint32_t": 'UInt32',
    "long long": 'SInt64',
    "int64_t": 'SInt64',
    "unsigned long long": 'UInt64',
    "uint64_t": 'UInt64',
    "size_t": 'UInt64',
    "ptrdiff_t": 'UInt64',
    "float": 'Float32',
    "double": 'Float64',
    #######################################################################
    # Warning: Linux + OS X ONLY
    # On Windows, these are 64-bit.  Not sure what to do about this.
    "long": 'SInt32',           
    "unsigned long": 'UInt32',
    #######################################################################
    }

  kl_type_name_to_cpp_type_expr = {
    "Boolean": Bool(),
    "SInt8": Named([Simple("int8_t")]),
    "UInt8": Named([Simple("uint8_t")]),
    "SInt16": Named([Simple("int16_t")]),
    "UInt16": Named([Simple("uint16_t")]),
    "SInt32": Named([Simple("int32_t")]),
    "UInt32": Named([Simple("uint32_t")]),
    "SInt64": Named([Simple("int64_t")]),
    "UInt64": Named([Simple("uint64_t")]),
    "Float32": Float(),
    "Float64": Double(),
    }

  dq_desc_to_ti_class = {
    'direct': SimpleDirectTypeInfo,
    'const_ref': SimpleConstRefTypeInfo,
    'mutable_ref': SimpleMutableRefTypeInfo,
    'const_ptr': SimpleConstPtrTypeInfo,
    'mutable_ptr': SimpleMutablePtrTypeInfo,
    }

  def __init__(self, ext):
    Selector.__init__(self, ext)
    self.ti_cache = {}
    self.decl_cache = {}

  def get_desc(self):
    return "Simple"
  
  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    undq_cpp_type_expr, dq = cpp_type_expr.get_undq()
    kl_type_name = self.cpp_type_name_to_kl_type_name.get(str(undq_cpp_type_expr))
    if kl_type_name:
      ti_cache_key = "%s:%s" % (dq.get_desc(), kl_type_name)
      ti = self.ti_cache.get(ti_cache_key)
      if not ti:
        undq_cpp_type_expr = self.kl_type_name_to_cpp_type_expr[kl_type_name]
        ti = self.dq_desc_to_ti_class[dq.get_desc()](self.jinjenv, kl_type_name, undq_cpp_type_expr)
        self.ti_cache.setdefault(ti_cache_key, ti)
      decl_cache_key = kl_type_name
      decl = self.decl_cache.get(decl_cache_key)
      if not decl:
        decl = SimpleBuiltinDecl(self.ext, kl_type_name, undq_cpp_type_expr)
        self.decl_cache.setdefault(decl_cache_key, decl)
        self.ext.decls.append(decl)
      return DirQualTypeInfo(DirQual(directions.Direct, qualifiers.Unqualified), ti)
