#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.cpp_type_expr_parser import dir_qual
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *
from libkludge.generate.builtin_decl import BuiltinDecl

builtin_kl_type_names = [
  'Boolean',
  'SInt8',
  'UInt8',
  'SInt16',
  'UInt16',
  'SInt32',
  'UInt32',
  'SInt64',
  'UInt64',
  'Float32',
  'Float64',
  ]

def build_edk_name(kl_type_name):
  if kl_type_name in builtin_kl_type_names:
    return "Fabric::EDK::KL::" + kl_type_name
  else:
    return "Fabric_EDK_KL_" + kl_type_name

class InPlaceTypeInfo(TypeInfo):

  def __init__(
    self,
    jinjenv,
    kl_type_name,
    cpp_type_expr,
    extends,
    record,
    is_simple,
    ):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base=kl_type_name,
      edk_name=build_edk_name(kl_type_name),
      lib_expr=cpp_type_expr,
      extends=extends,
      record=record,
      is_simple=is_simple,
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    if self.is_simple:
      tds["conv"]["*"] = "types/builtin/in_place/simple/conv"
      tds["result"]["*"] = "protocols/result/builtin/direct"
      tds["repr"]["*"] = "protocols/repr/builtin/in_place"
      tds["repr"]["new_begin"] = "types/builtin/in_place/simple/repr"
    else:
      tds["conv"]["*"] = "protocols/conv/builtin/none"
      tds["result"]["*"] = "protocols/result/builtin/indirect"
      tds["result"]["decl_and_assign_lib_begin"] = "types/builtin/in_place/complex/result"
      tds["result"]["decl_and_assign_lib_end"] = "types/builtin/in_place/complex/result"
      tds["result"]["indirect_lib_to_edk"] = "types/builtin/in_place/complex/result"
      tds["repr"]["*"] = "protocols/repr/builtin/in_place"
    return tds

class InPlaceBuiltinDecl(BuiltinDecl):

  def __init__(self, ext, is_simple, type_info):
    BuiltinDecl.__init__(
      self,
      ext.root_namespace,
      desc="InPlace %s" % (type_info),
      template_path="types/builtin/in_place/in_place",
      test_name="InPlace_%s" % (type_info.kl.name),
      )
    self.is_simple = is_simple
    self.type_info = type_info

  def render_method_impls(self, lang):
    result = ''
    if self.type_info.record:
      result += self.type_info.record.render('impls', lang, {
        'type_info': self.type_info,
        'is_direct': True,
        'is_const_ptr': False,
        'is_mutable_ptr': False,
        'is_const_ref': False,
        'is_mutable_ref': False,
        'allow_static_methods': True,
        'allow_mutable_methods': True,
        'allow_const_methods': True,
        'is_ptr': False,
        })
    return result

class InPlaceSpec(object):

  def __init__(self, kl_type_name, cpp_type_expr, extends, record, is_simple=False):
    self.kl_type_name = kl_type_name
    self.cpp_type_expr = cpp_type_expr
    self.is_simple = is_simple
    self.extends = extends
    self.record = record

class InPlaceSelector(Selector):

  should_create_ptr_ref = True

  def __init__(self, ext):
    Selector.__init__(self, ext)

    boolean_spec = InPlaceSpec("Boolean", Bool(), None, None, True)
    char_spec = InPlaceSpec("CxxChar", Char(), None, None, True)
    sint8_spec = InPlaceSpec("SInt8", SimpleNamed("int8_t"), None, None, True)
    uint8_spec = InPlaceSpec("UInt8", SimpleNamed("uint8_t"), None, None, True)
    sint16_spec = InPlaceSpec("SInt16", SimpleNamed("int16_t"), None, None, True)
    uint16_spec = InPlaceSpec("UInt16", SimpleNamed("uint16_t"), None, None, True)
    sint32_spec = InPlaceSpec("SInt32", SimpleNamed("int32_t"), None, None, True)
    uint32_spec = InPlaceSpec("UInt32", SimpleNamed("uint32_t"), None, None, True)
    sint64_spec = InPlaceSpec("SInt64", SimpleNamed("int64_t"), None, None, True)
    uint64_spec = InPlaceSpec("UInt64", SimpleNamed("uint64_t"), None, None, True)
    float32_spec = InPlaceSpec("Float32", Float(), None, None, True)
    float64_spec = InPlaceSpec("Float64", Double(), None, None, True)

    self.cpp_type_expr_to_spec = {
      Bool(): boolean_spec,
      Char(): char_spec,
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

    self.type_info_cache = {}

  def get_desc(self):
    return "InPlace"

  def register(self, kl_type_name, cpp_type_expr, extends, record):
    self.cpp_type_expr_to_spec[cpp_type_expr] = InPlaceSpec(
      kl_type_name, cpp_type_expr, extends, record
      )
  
  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    undq_cpp_type_expr, dq = cpp_type_expr.get_undq()
    if dq.is_direct:
      spec = self.cpp_type_expr_to_spec.get(undq_cpp_type_expr)
      if spec:
        kl_type_name = spec.kl_type_name
        undq_cpp_type_expr = spec.cpp_type_expr
        is_simple = spec.is_simple
        extends = spec.extends
        record = spec.record

        type_info_cache_key = kl_type_name
        type_info = self.type_info_cache.get(type_info_cache_key)
        if not type_info:
          type_info = InPlaceTypeInfo(
            self.jinjenv,
            kl_type_name,
            undq_cpp_type_expr,
            extends=extends,
            record=record,
            is_simple=is_simple,
            )
          self.type_info_cache.setdefault(type_info_cache_key, type_info)
          self.ext.decls.append(InPlaceBuiltinDecl(self.ext, is_simple, type_info))

        return DirQualTypeInfo(dq, type_info)
