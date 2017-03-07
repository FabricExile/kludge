#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.type_simplifier import NullTypeSimplifier
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
    kl_type_name_for_derivatives,
    cpp_type_expr,
    extends,
    record,
    is_simple,
    forbid_copy,
    simplifier,
    ):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base=kl_type_name,
      kl_name_base_for_derivatives=kl_type_name_for_derivatives,
      edk_name=build_edk_name(kl_type_name),
      lib_expr=cpp_type_expr,
      extends=extends,
      record=record,
      is_simple=is_simple,
      forbid_copy=forbid_copy,
      simplifier=simplifier,
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

  def __init__(
    self,
    kl_type_name,
    cpp_type_expr,
    extends,
    record,
    is_simple=False,
    kl_type_name_for_derivatives=None,
    forbid_copy=False,
    simplifier=NullTypeSimplifier(),
    ):
    self.kl_type_name = kl_type_name
    if not kl_type_name_for_derivatives:
      kl_type_name_for_derivatives = kl_type_name
    self.kl_type_name_for_derivatives = kl_type_name_for_derivatives
    self.cpp_type_expr = cpp_type_expr
    self.is_simple = is_simple
    self.extends = extends
    self.record = record
    self.forbid_copy = forbid_copy
    self.simplifier = simplifier

class InPlaceSelector(Selector):

  def __init__(self, ext):
    Selector.__init__(self, ext)

    self.cpp_type_expr_to_spec = {
      Bool(): InPlaceSpec("Boolean", Bool(), None, None, True),
      Char(): InPlaceSpec("CxxChar", Char(), None, None, True),
      SimpleNamed("int8_t"): InPlaceSpec("SInt8", SimpleNamed("int8_t"), None, None, True),
      Unsigned(Char()): InPlaceSpec("UInt8", SimpleNamed("uint8_t"), None, None, True),
      SimpleNamed("uint8_t"): InPlaceSpec("UInt8", SimpleNamed("uint8_t"), None, None, True),
      Short(): InPlaceSpec("SInt16", SimpleNamed("int16_t"), None, None, True),
      SimpleNamed("int16_t"): InPlaceSpec("SInt16", SimpleNamed("int16_t"), None, None, True),
      Unsigned(Short()): InPlaceSpec("UInt16", SimpleNamed("uint16_t"), None, None, True),
      SimpleNamed("uint16_t"): InPlaceSpec("UInt16", SimpleNamed("uint16_t"), None, None, True),
      Int(): InPlaceSpec("SInt32", SimpleNamed("int32_t"), None, None, True),
      SimpleNamed("int32_t"): InPlaceSpec("SInt32", SimpleNamed("int32_t"), None, None, True),
      Unsigned(Int()): InPlaceSpec("UInt32", SimpleNamed("uint32_t"), None, None, True),
      SimpleNamed("uint32_t"): InPlaceSpec("UInt32", SimpleNamed("uint32_t"), None, None, True),
      LongLong(): InPlaceSpec("SInt64", LongLong(), None, None, True),
      SimpleNamed("int64_t"): InPlaceSpec("SInt64", SimpleNamed("int64_t"), None, None, True),
      Unsigned(LongLong()): InPlaceSpec("UInt64", Unsigned(LongLong()), None, None, True),
      SimpleNamed("uint64_t"): InPlaceSpec("UInt64", SimpleNamed("uint64_t"), None, None, True),
      SimpleNamed("size_t"): InPlaceSpec("UInt64", SimpleNamed("size_t"), None, None, True),
      SimpleNamed("ptrdiff_t"): InPlaceSpec("UInt64", SimpleNamed("ptrdiff_t"), None, None, True),
      SimpleNamed("intptr_t"): InPlaceSpec("UInt64", SimpleNamed("intptr_t"), None, None, True),
      Float(): InPlaceSpec("Float32", Float(), None, None, True),
      Double(): InPlaceSpec("Float64", Double(), None, None, True),
      #######################################################################
      # Warning: Linux + OS X ONLY
      # On Windows, these are 64-bit.  Not sure what to do about this.
      Long(): InPlaceSpec("SInt64", Long(), None, None, True),           
      Unsigned(Long()): InPlaceSpec("UInt64", Unsigned(Long()), None, None, True),
      #######################################################################
      }

    self.type_info_cache = {}

  def get_desc(self):
    return "InPlace"

  def register(
    self,
    kl_type_name,
    kl_type_name_for_derivatives,
    cpp_type_expr,
    extends,
    record,
    forbid_copy=False,
    dont_delete=False,
    simplifier=None,
    ):
    self.cpp_type_expr_to_spec[cpp_type_expr] = InPlaceSpec(
      kl_type_name,
      cpp_type_expr,
      extends,
      record,
      kl_type_name_for_derivatives=kl_type_name_for_derivatives,
      forbid_copy=forbid_copy,
      simplifier=simplifier,
      )
  
  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    undq_cpp_type_expr, dq = cpp_type_expr.get_undq()
    if dq.is_direct:
      spec = self.cpp_type_expr_to_spec.get(undq_cpp_type_expr)
      if spec:
        kl_type_name = spec.kl_type_name
        kl_type_name_for_derivatives = spec.kl_type_name_for_derivatives
        undq_cpp_type_expr = spec.cpp_type_expr
        is_simple = spec.is_simple
        extends = spec.extends
        record = spec.record
        forbid_copy = spec.forbid_copy
        simplifier = spec.simplifier

        type_info_cache_key = kl_type_name
        type_info = self.type_info_cache.get(type_info_cache_key)
        if not type_info:
          type_info = InPlaceTypeInfo(
            self.jinjenv,
            kl_type_name,
            kl_type_name_for_derivatives,
            undq_cpp_type_expr,
            extends=extends,
            record=record,
            is_simple=is_simple,
            forbid_copy=forbid_copy,
            simplifier=simplifier,
            )
          self.type_info_cache.setdefault(type_info_cache_key, type_info)
          self.ext.add_decl(InPlaceBuiltinDecl(self.ext, is_simple, type_info))

        return DirQualTypeInfo(dq, type_info)
