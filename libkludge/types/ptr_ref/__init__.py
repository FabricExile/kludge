#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo, KLTypeName
from libkludge.type_simplifier import TypeSimplifier
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
  else:
    return 'Cxx' + kl_type_name + suffix

def build_edk_name(kl_type_name, suffix):
  if kl_type_name.startswith('Cxx'):
    return kl_type_name + suffix
  else:
    return 'Cxx' + kl_type_name + suffix

class PtrRefTypeSimplifier(TypeSimplifier):

  def __init__(self, direct_type_info):
    TypeSimplifier.__init__(self)
    self.direct_type_info = direct_type_info.from_derivative
    self.direct_type_info_for_derivatives = direct_type_info

  def render_kl_to_cxx(self, ti, kl_vn, cxx_vn):
    return cxx_vn + " = Make_" + ti.kl.name.compound + "(" + kl_vn + ");"

  def render_decl_kl_to_cxx(self, ti, kl_vn, cxx_vn):
    return ti.kl.name.compound + " " + self.render_kl_to_cxx(ti, kl_vn, cxx_vn)

  def param_cost(self, type_info):
    return self.direct_type_info.simplifier.param_cost(self.direct_type_info)

  def param_type_name(self, type_info):
    return self.direct_type_info.simplifier.param_type_name(self.direct_type_info)

  def child_param_cxx_value_name(self, ti, kl_vn):
    return self.direct_type_info.simplifier.param_cxx_value_name(self.direct_type_info, kl_vn)

  def param_cxx_value_name(self, ti, kl_vn):
    child_cxx_vn = self.child_param_cxx_value_name(ti, kl_vn)
    return child_cxx_vn + "__cxx"

  def render_param_pre(self, ti, kl_vn):
    child_cxx_vn = self.child_param_cxx_value_name(ti, kl_vn)
    cxx_vn = self.param_cxx_value_name(ti, kl_vn)
    return '\n'.join([
      self.direct_type_info.simplifier.render_param_pre(self.direct_type_info, kl_vn),
      self.render_decl_kl_to_cxx(ti, child_cxx_vn, cxx_vn),
      ])

  def result_kl_type_name(self, ti):
    return self.direct_type_info.simplifier.result_kl_type_name(self.direct_type_info)

  def result_cxx_value_name(self, ti, kl_vn):
    return self.direct_type_info.simplifier.result_cxx_value_name(self.direct_type_info, kl_vn) + "_cxx"

  def render_result_decl_cxx_to_kl(self, ti, kl_vn):
    src_vn = self.result_cxx_value_name(ti, kl_vn)
    dst_vn = self.direct_type_info.simplifier.result_cxx_value_name(self.direct_type_info, kl_vn)
    return '\n'.join([
      self.render_decl_cxx_to_kl(ti, src_vn, dst_vn),
      self.direct_type_info.simplifier.render_result_decl_cxx_to_kl(self.direct_type_info, kl_vn),
      ])

class PtrTypeSimplifier(PtrRefTypeSimplifier):

  def __init__(self, direct_type_info):
    PtrRefTypeSimplifier.__init__(self, direct_type_info)

  def render_decl_cxx_to_kl(self, ti, src_vn, dst_vn):
    dst_tn = self.direct_type_info.kl.name
    src_tn = ti.kl.name
    return '\n'.join([
      "if (Fabric_Guarded && !" + src_vn + ".cxx_isValid())",
      "  throw 'Call of cxx_deref() on null " + src_tn.compound + "';",
      dst_tn.base + " " + dst_vn + dst_tn.suffix + " = " + src_vn + ".cxx_deref().cxx_get();",
      ])

class RefTypeSimplifier(PtrRefTypeSimplifier):

  def __init__(self, direct_type_info):
    PtrRefTypeSimplifier.__init__(self, direct_type_info)

  def render_decl_cxx_to_kl(self, ti, src_vn, dst_vn):
    dst_tn = self.direct_type_info.kl.name
    src_tn = ti.kl.name
    return '\n'.join([
      "// if (Fabric_Guarded && !" + src_vn + ".cxx_isValid())",
      "//   throw 'Call of cxx_deref() on null " + src_tn.compound + "';",
      dst_tn.base + " " + dst_vn + dst_tn.suffix + " = " + src_vn + ".cxx_get();",
      ])

class ConstRefTypeSimplifier(RefTypeSimplifier):

  def __init__(self, direct_type_info):
    RefTypeSimplifier.__init__(self, direct_type_info)

  def render_param_post(self, ti, vn):
    return self.direct_type_info.simplifier.render_param_post(ti, vn)

class ConstRefTypeInfo(TypeInfo):

  def __init__(self, jinjenv, undq_type_info, undq_orig_type_info):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base=build_kl_name_base(undq_type_info.kl.name.compound, 'ConstRef'),
      edk_name=build_edk_name(undq_type_info.kl.name.compound, 'ConstRef'),
      lib_expr=ReferenceTo(Const(undq_type_info.lib.expr)),
      record=undq_type_info.record,
      is_simple=undq_type_info.is_simple,
      direct_type_info=undq_type_info,
      direct_orig_type_info=undq_orig_type_info,
      is_const_ref=True,
      simplifier=ConstRefTypeSimplifier(undq_type_info),
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "types/builtin/ptr_ref/ref/conv"
    tds["result"]["*"] = "protocols/result/builtin/indirect"
    tds["repr"]["new_begin"] = "types/builtin/ptr_ref/ref/repr"
    tds["repr"]["validate_edk"] = "types/builtin/ptr_ref/ref/repr"
    return tds

class MutableRefTypeSimplifier(RefTypeSimplifier):

  def __init__(self, direct_type_info):
    RefTypeSimplifier.__init__(self, direct_type_info)

  def render_param_post(self, ti, vn):
    return '\n'.join([
      self.direct_type_info.simplifier.render_param_copy_back(self.direct_type_info, vn),
      ])

  def render_param_pass_type(self, type_info):
    return "io"

class MutableRefTypeInfo(TypeInfo):

  def __init__(self, jinjenv, undq_type_info, undq_orig_type_info):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base=build_kl_name_base(undq_type_info.kl.name.compound, 'Ref'),
      edk_name=build_edk_name(undq_type_info.kl.name.compound, 'MutableRef'),
      lib_expr=ReferenceTo(undq_type_info.lib.expr),
      record=undq_type_info.record,
      is_simple=undq_type_info.is_simple,
      direct_type_info=undq_type_info,
      direct_orig_type_info=undq_orig_type_info,
      simplifier=MutableRefTypeSimplifier(undq_type_info),
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "types/builtin/ptr_ref/ref/conv"
    tds["result"]["*"] = "protocols/result/builtin/indirect"
    tds["repr"]["new_begin"] = "types/builtin/ptr_ref/ref/repr"
    tds["repr"]["validate_edk"] = "types/builtin/ptr_ref/ref/repr"
    return tds

class ConstPtrTypeSimplifier(PtrTypeSimplifier):

  def __init__(self, direct_type_info):
    PtrTypeSimplifier.__init__(self, direct_type_info)

  def param_type_name(self, ti):
    if self.direct_type_info.kl.name.base == 'CxxChar':
      return KLTypeName("String", "")
    return PtrTypeSimplifier.param_type_name(self, ti)

  def render_param_pre(self, ti, kl_vn):
    if self.direct_type_info.kl.name.base == 'CxxChar':
      cxx_vn = self.param_cxx_value_name(self, kl_vn)
      return "CxxCharConstPtr " + cxx_vn + " = CxxCharConstPtr(" + kl_vn + ");"
    return PtrTypeSimplifier.render_param_pre(self, ti, kl_vn)

  def param_cxx_value_name(self, ti, kl_vn):
    if self.direct_type_info.kl.name.base == 'CxxChar':
      return kl_vn + "__cxx"
    return PtrTypeSimplifier.param_cxx_value_name(self, ti, kl_vn)

  def render_param_post(self, ti, vn):
    return self.direct_type_info.simplifier.render_param_post(self.direct_type_info, vn)

  def result_kl_type_name(self, ti):
    if self.direct_type_info.kl.name.base == 'CxxChar':
      return KLTypeName("String", "")
    return PtrTypeSimplifier.result_kl_type_name(self, ti)

  def result_cxx_value_name(self, ti, kl_vn):
    if self.direct_type_info.kl.name.base == 'CxxChar':
      return TypeSimplifier.result_cxx_value_name(self, ti, kl_vn)
    return PtrTypeSimplifier.result_cxx_value_name(self, ti, kl_vn)

  def render_result_decl_cxx_to_kl(self, ti, kl_vn):
    if self.direct_type_info.kl.name.base == 'CxxChar':
      return TypeSimplifier.render_result_decl_cxx_to_kl(self, ti, kl_vn)
    return PtrTypeSimplifier.render_result_decl_cxx_to_kl(self, ti, kl_vn)

class ConstPtrTypeInfo(TypeInfo):

  def __init__(self, jinjenv, undq_type_info, undq_orig_type_info):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base=build_kl_name_base(undq_type_info.kl.name.compound, 'ConstPtr'),
      edk_name=build_edk_name(undq_type_info.kl.name.compound, 'ConstPtr'),
      lib_expr=PointerTo(Const(undq_type_info.lib.expr)),
      record=undq_type_info.record,
      is_simple=undq_type_info.is_simple,
      direct_type_info=undq_type_info,
      direct_orig_type_info=undq_orig_type_info,
      simplifier=ConstPtrTypeSimplifier(undq_type_info),
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "types/builtin/ptr_ref/ptr/conv"
    tds["result"]["*"] = "protocols/result/builtin/indirect"
    tds["repr"]["new_begin"] = "types/builtin/ptr_ref/ptr/repr"
    return tds

class MutablePtrTypeSimplifier(PtrTypeSimplifier):

  def __init__(self, direct_type_info):
    PtrTypeSimplifier.__init__(self, direct_type_info)

  def render_param_post(self, ti, vn):
    return '\n'.join([
      self.direct_type_info.simplifier.render_param_copy_back(self.direct_type_info, vn),
      ])

  def render_param_pass_type(self, type_info):
    return "io"

class MutablePtrTypeInfo(TypeInfo):

  def __init__(self, jinjenv, undq_type_info, undq_orig_type_info):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base=build_kl_name_base(undq_type_info.kl.name.compound, 'Ptr'),
      edk_name=build_edk_name(undq_type_info.kl.name.compound, 'MutablePtr'),
      lib_expr=PointerTo(undq_type_info.lib.expr),
      record=undq_type_info.record,
      is_simple=undq_type_info.is_simple,
      direct_type_info=undq_type_info,
      direct_orig_type_info=undq_orig_type_info,
      simplifier=MutablePtrTypeSimplifier(undq_type_info),
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "types/builtin/ptr_ref/ptr/conv"
    tds["result"]["*"] = "protocols/result/builtin/indirect"
    tds["repr"]["new_begin"] = "types/builtin/ptr_ref/ptr/repr"
    return tds

type_info_class_map = {
  'const_ref': ConstRefTypeInfo,
  'mutable_ref': MutableRefTypeInfo,
  'const_ptr': ConstPtrTypeInfo,
  'mutable_ptr': MutablePtrTypeInfo,
  }

class PtrRefBuiltinDecl(BuiltinDecl):

  def __init__(
    self,
    ext,
    ti_set,
    is_kludge_ext,
    ):
    BuiltinDecl.__init__(
      self,
      ext.root_namespace,
      desc="PtrRef %s" % (ti_set.direct),
      template_path="types/builtin/ptr_ref/ptr_ref",
      test_name="PtrRef_%s" % (ti_set.direct.kl.name),
      is_kludge_ext=is_kludge_ext,
      )
    self.type_info = ti_set

  def render_method_impls(self, lang):
    result = ''
    if self.type_info.direct.record:
      records = self.type_info.direct.record.get_nested_records()
      for index, type_info in enumerate([
        self.type_info.const_ptr,
        self.type_info.mutable_ptr,
        self.type_info.const_ref,
        self.type_info.mutable_ref,
        ]):
        for ri in range(0, len(records)):
          record = records[ri]
          is_direct = False
          is_const_ptr = index == 0
          is_mutable_ptr = index == 1
          is_const_ref = index == 2
          is_mutable_ref = index == 3
          result += record.render('impls', lang, {
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
            'is_final_record': ri == len(records) - 1,
            })
    return result

class PtrRefTypeInfoSet(object):
  
  def __init__(self, jinjenv, undq_type_info):
    self.direct = undq_type_info
    undq_type_info_for_derivatives = undq_type_info.for_derivatives()
    for name, klass in type_info_class_map.iteritems():
      setattr(self, name, klass(jinjenv, undq_type_info_for_derivatives, undq_type_info))

  def get_indirects(self):
    return [self.const_ptr, self.mutable_ptr, self.const_ref, self.mutable_ref]

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
          self.ext.add_decl(PtrRefBuiltinDecl(
            self.ext,
            ti_set,
            is_kludge_ext=self.is_kludge_ext_cpp_type_expr(cpp_type_expr),
            ))

        ti = getattr(ti_set, dq.get_desc())
        return DirQualTypeInfo(DirQual(directions.Direct, qualifiers.Unqualified), ti)
