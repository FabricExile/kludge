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

def build_kl_name_base(kl_type_name, suffix):
  if kl_type_name.startswith('Cxx'):
    return kl_type_name + suffix
  return kl_type_name + '_Cxx' + suffix

def build_edk_name(kl_type_name, suffix):
  if kl_type_name.startswith('Cxx'):
    return kl_type_name + suffix
  return kl_type_name + '_Cxx' + suffix

class ConstRefTypeInfo(TypeInfo):

  def __init__(self, jinjenv, undq_type_info):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base=build_kl_name_base(undq_type_info.kl.name.compound, 'ConstRef'),
      edk_name=build_edk_name(undq_type_info.kl.name.compound, 'ConstRef'),
      lib_expr=ReferenceTo(Const(undq_type_info.lib.expr)),
      record=undq_type_info.record,
      is_simple=undq_type_info.is_simple,
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "types/builtin/ptr_ref/ref/conv"
    tds["result"]["*"] = "protocols/result/builtin/indirect"
    return tds

class MutableRefTypeInfo(TypeInfo):

  def __init__(self, jinjenv, undq_type_info):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base=build_kl_name_base(undq_type_info.kl.name.compound, 'Ref'),
      edk_name=build_edk_name(undq_type_info.kl.name.compound, 'MutableRef'),
      lib_expr=ReferenceTo(undq_type_info.lib.expr),
      record=undq_type_info.record,
      is_simple=undq_type_info.is_simple,
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "types/builtin/ptr_ref/ref/conv"
    tds["result"]["*"] = "protocols/result/builtin/indirect"
    return tds

class ConstPtrTypeInfo(TypeInfo):

  def __init__(self, jinjenv, undq_type_info):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base=build_kl_name_base(undq_type_info.kl.name.compound, 'ConstPtr'),
      edk_name=build_edk_name(undq_type_info.kl.name.compound, 'ConstPtr'),
      lib_expr=PointerTo(Const(undq_type_info.lib.expr)),
      record=undq_type_info.record,
      is_simple=undq_type_info.is_simple,
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "types/builtin/ptr_ref/ptr/conv"
    tds["result"]["*"] = "protocols/result/builtin/indirect"
    return tds

class MutablePtrTypeInfo(TypeInfo):

  def __init__(self, jinjenv, undq_type_info):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base=build_kl_name_base(undq_type_info.kl.name.compound, 'Ptr'),
      edk_name=build_edk_name(undq_type_info.kl.name.compound, 'MutablePtr'),
      lib_expr=PointerTo(undq_type_info.lib.expr),
      record=undq_type_info.record,
      is_simple=undq_type_info.is_simple,
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "types/builtin/ptr_ref/ptr/conv"
    tds["result"]["*"] = "protocols/result/builtin/indirect"
    return tds

type_info_class_map = {
  'const_ref': ConstRefTypeInfo,
  'mutable_ref': MutableRefTypeInfo,
  'const_ptr': ConstPtrTypeInfo,
  'mutable_ptr': MutablePtrTypeInfo,
  }

class PtrRefBuiltinDecl(BuiltinDecl):

  def __init__(self, ext, ti_set):
    BuiltinDecl.__init__(
      self,
      ext.root_namespace,
      desc="PtrRef %s" % (ti_set.direct),
      template_path="types/builtin/ptr_ref/ptr_ref",
      test_name="PtrRef_%s" % (ti_set.direct.kl.name),
      )
    self.type_info = ti_set

  def render_method_impls(self, lang):
    result = ''
    for index, type_info in enumerate([
      self.type_info.const_ptr,
      self.type_info.mutable_ptr,
      self.type_info.const_ref,
      self.type_info.mutable_ref,
      ]):
      if type_info.record:
        is_direct = False
        is_const_ptr = index == 0
        is_mutable_ptr = index == 1
        is_const_ref = index == 2
        is_mutable_ref = index == 3
        result += type_info.record.render('impls', lang, {
          'type_info': type_info,
          'is_direct': is_direct,
          'is_const_ptr': is_const_ptr,
          'is_mutable_ptr': is_mutable_ptr,
          'is_const_ref': is_const_ref,
          'is_mutable_ref': is_mutable_ref,
          'allow_static_methods': is_direct,
          'allow_mutable_methods': is_direct or is_mutable_ptr or is_mutable_ref,
          'allow_const_methods': True,
          'is_ptr': is_const_ptr or is_mutable_ptr,
          })
    return result

class PtrRefTypeInfoSet(object):
  
  def __init__(self, jinjenv, undq_type_info):
    self.direct = undq_type_info
    for name, klass in type_info_class_map.iteritems():
      setattr(self, name, klass(jinjenv, undq_type_info))

class PtrRefSelector(Selector):

  def __init__(self, ext):
    Selector.__init__(self, ext)
    self.ti_set_cache = {}

  def get_desc(self):
    return "PtrRef"

  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    undq_cpp_type_expr, dq = cpp_type_expr.get_undq()
    if not dq.is_direct:
      undq_dqti = type_mgr.maybe_get_dqti(undq_cpp_type_expr)
      if undq_dqti:
        undq_type_info = undq_dqti.type_info
        kl_type_name = undq_type_info.kl.name.compound

        ti_set_cache_key = kl_type_name
        ti_set = self.ti_set_cache.get(ti_set_cache_key)
        if not ti_set:
          ti_set = PtrRefTypeInfoSet(
            self.jinjenv,
            undq_type_info,
            )
          self.ti_set_cache.setdefault(ti_set_cache_key, ti_set)
          self.ext.decls.append(PtrRefBuiltinDecl(self.ext, ti_set))

        ti = getattr(ti_set, dq.get_desc())
        return DirQualTypeInfo(DirQual(directions.Direct, qualifiers.Unqualified), ti)