#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.cpp_type_expr_parser import dir_qual
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *
from libkludge.generate.builtin_decl import BuiltinDecl

class InPlaceDirectTypeInfo(TypeInfo):

  def __init__(self, jinjenv, kl_type_name, undq_cpp_type_expr, is_simple):
    if is_simple:
      edk_name = "Fabric::EDK::KL::" + kl_type_name
    else:
      edk_name = "Fabric_EDK_KL_" + kl_type_name
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base = kl_type_name,
      edk_name = edk_name,
      lib_expr = undq_cpp_type_expr,
      )
    self.is_simple = is_simple

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    if self.is_simple:
      tds["conv"]["*"] = "types/builtin/in_place/direct/simple/conv"
      tds["result"]["*"] = "protocols/result/builtin/direct"
      tds["repr"]["new_begin"] = "types/builtin/in_place/direct/simple/repr"
    else:
      tds["conv"]["*"] = "protocols/conv/builtin/none"
      tds["result"]["*"] = "protocols/result/builtin/indirect"
      tds["result"]["decl_and_assign_lib_begin"] = "types/builtin/in_place/direct/complex/result"
      tds["result"]["decl_and_assign_lib_end"] = "types/builtin/in_place/direct/complex/result"
      tds["result"]["indirect_lib_to_edk"] = "types/builtin/in_place/direct/complex/result"
    return tds

class InPlaceConstRefTypeInfo(TypeInfo):

  def __init__(self, jinjenv, kl_type_name, undq_cpp_type_expr, is_simple):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base = kl_type_name + "ConstRef",
      edk_name = "Fabric_EDK_KL_" + kl_type_name + "ConstRef",
      lib_expr = ReferenceTo(Const(undq_cpp_type_expr)),
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "types/builtin/in_place/ref/conv"
    tds["result"]["*"] = "protocols/result/builtin/indirect"
    return tds

class InPlaceMutableRefTypeInfo(TypeInfo):

  def __init__(self, jinjenv, kl_type_name, undq_cpp_type_expr, is_simple):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base = kl_type_name + "Ref",
      edk_name = "Fabric_EDK_KL_" + kl_type_name + "MutableRef",
      lib_expr = ReferenceTo(undq_cpp_type_expr),
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "types/builtin/in_place/ref/conv"
    tds["result"]["*"] = "protocols/result/builtin/indirect"
    return tds

class InPlaceConstPtrTypeInfo(TypeInfo):

  def __init__(self, jinjenv, kl_type_name, undq_cpp_type_expr, is_simple):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base = kl_type_name + "ConstPtr",
      edk_name = "Fabric_EDK_KL_" + kl_type_name + "ConstPtr",
      lib_expr = PointerTo(Const(undq_cpp_type_expr)),
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "types/builtin/in_place/ptr/conv"
    tds["result"]["*"] = "protocols/result/builtin/indirect"
    return tds

class InPlaceMutablePtrTypeInfo(TypeInfo):

  def __init__(self, jinjenv, kl_type_name, undq_cpp_type_expr, is_simple):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base = kl_type_name + "Ptr",
      edk_name = "Fabric_EDK_KL_" + kl_type_name + "MutablePtr",
      lib_expr = PointerTo(undq_cpp_type_expr),
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "types/builtin/in_place/ptr/conv"
    tds["result"]["*"] = "protocols/result/builtin/indirect"
    return tds

class InPlaceBuiltinDecl(BuiltinDecl):

  def __init__(self, ext, kl_type_name, cpp_type_expr, is_simple):
    BuiltinDecl.__init__(
      self,
      ext.root_namespace,
      desc="InPlace %s" % (kl_type_name),
      template_path="types/builtin/in_place/in_place",
      test_name="InPlace_%s" % (kl_type_name),
      )
    self.kl_type_name = kl_type_name
    self.cpp_type_expr = cpp_type_expr
    self.is_simple = is_simple

class InPlaceSpec(object):

  def __init__(self, kl_type_name, cpp_type_expr, is_simple):
    self.kl_type_name = kl_type_name
    self.cpp_type_expr = cpp_type_expr
    self.is_simple = is_simple

class InPlaceSelector(Selector):

  dq_desc_to_ti_class = {
    'direct': InPlaceDirectTypeInfo,
    'const_ref': InPlaceConstRefTypeInfo,
    'mutable_ref': InPlaceMutableRefTypeInfo,
    'const_ptr': InPlaceConstPtrTypeInfo,
    'mutable_ptr': InPlaceMutablePtrTypeInfo,
    }

  def __init__(self, ext):
    Selector.__init__(self, ext)

    boolean_spec = InPlaceSpec("Boolean", Bool(), True)
    sint8_spec = InPlaceSpec("SInt8", SimpleNamed("int8_t"), True)
    uint8_spec = InPlaceSpec("UInt8", SimpleNamed("uint8_t"), True)
    sint16_spec = InPlaceSpec("SInt16", SimpleNamed("int16_t"), True)
    uint16_spec = InPlaceSpec("UInt16", SimpleNamed("uint16_t"), True)
    sint32_spec = InPlaceSpec("SInt32", SimpleNamed("int32_t"), True)
    uint32_spec = InPlaceSpec("UInt32", SimpleNamed("uint32_t"), True)
    sint64_spec = InPlaceSpec("SInt64", SimpleNamed("int64_t"), True)
    uint64_spec = InPlaceSpec("UInt64", SimpleNamed("uint64_t"), True)
    float32_spec = InPlaceSpec("Float32", Float(), True)
    float64_spec = InPlaceSpec("Float64", Double(), True)

    self.cpp_type_expr_to_spec = {
      Bool(): boolean_spec,
      Char(): sint8_spec,
      SimpleNamed("int8_t"): sint8_spec,
      Unsigned(Char()): uint8_spec,
      SimpleNamed("uint8_t"): uint8_spec,
      Short(): sint16_spec,
      SimpleNamed("int16_t"): sint16_spec,
      Unsigned(Short()): uint16_spec,
      SimpleNamed("uint16_t"): uint16_spec,
      Int(): sint32_spec,
      SimpleNamed("int32_t"): sint32_spec,
      Unsigned(Int()): uint32_spec,
      SimpleNamed("uint32_t"): uint32_spec,
      LongLong(): sint64_spec,
      SimpleNamed("int64_t"): sint64_spec,
      Unsigned(LongLong()): uint64_spec,
      SimpleNamed("uint64_t"): uint64_spec,
      SimpleNamed("size_t"): uint64_spec,
      SimpleNamed("ptrdiff_t"): uint64_spec,
      Float(): float32_spec,
      Double(): float64_spec,
      #######################################################################
      # Warning: Linux + OS X ONLY
      # On Windows, these are 64-bit.  Not sure what to do about this.
      Long(): sint32_spec,           
      Unsigned(Long()): uint32_spec,
      #######################################################################
      }

    self.ti_cache = {}
    self.decl_cache = {}

  def get_desc(self):
    return "InPlace"

  def register(self, kl_type_name, cpp_type_expr):
    self.cpp_type_expr_to_spec[cpp_type_expr] = InPlaceSpec(kl_type_name, cpp_type_expr, False)
  
  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    undq_cpp_type_expr, dq = cpp_type_expr.get_undq()

    spec = self.cpp_type_expr_to_spec.get(undq_cpp_type_expr)
    if spec:
      kl_type_name = spec.kl_type_name
      undq_cpp_type_expr = spec.cpp_type_expr
      is_simple = spec.is_simple

      ti_cache_key = "%s:%s" % (dq.get_desc(), kl_type_name)
      ti = self.ti_cache.get(ti_cache_key)
      if not ti:
        ti = self.dq_desc_to_ti_class[dq.get_desc()](self.jinjenv, kl_type_name, undq_cpp_type_expr, is_simple)
        self.ti_cache.setdefault(ti_cache_key, ti)

      decl_cache_key = kl_type_name
      decl = self.decl_cache.get(decl_cache_key)
      if not decl:
        decl = InPlaceBuiltinDecl(self.ext, kl_type_name, undq_cpp_type_expr, is_simple)
        self.decl_cache.setdefault(decl_cache_key, decl)
        self.ext.decls.append(decl)

      return DirQualTypeInfo(DirQual(directions.Direct, qualifiers.Unqualified), ti)
