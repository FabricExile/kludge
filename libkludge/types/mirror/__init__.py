#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *
from libkludge.generate.builtin_decl import BuiltinDecl
from libkludge.generate.record import Record

class MirrorTypeInfo(TypeInfo):

  def __init__(
    self,
    jinjenv,
    kl_global_name,
    cpp_global_expr,
    record,
    ):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base=kl_global_name,
      kl_name_base_for_derivatives=kl_global_name,
      edk_name="Fabric_EDK_KL_" + kl_global_name,
      lib_expr=cpp_global_expr,
      record=record,
      )

class MirrorBuiltinDecl(BuiltinDecl):

  def __init__(self, ext, type_info):
    BuiltinDecl.__init__(
      self,
      ext.root_namespace,
      desc="Mirror %s" % (type_info),
      template_path="types/builtin/mirror/mirror",
      test_name="Mirror_%s" % (type_info.kl.name),
      )
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

class MirrorSpec(object):

  def __init__(
    self,
    cpp_global_expr,
    kl_global_name,
    namespace,
    ):
    self.cpp_global_expr = cpp_global_expr
    self.kl_global_name = kl_global_name
    self.namespace = namespace

class MirrorSelector(Selector):

  should_create_ptr_ref = True

  def __init__(self, ext):
    Selector.__init__(self, ext)
    self.cpp_global_expr_to_spec = {}
    self.type_info_cache = {}

  def register(
    self,
    cpp_global_expr,
    kl_global_name,
    namespace,
    ):
    self.cpp_global_expr_to_spec[cpp_global_expr] = MirrorSpec(
      cpp_global_expr, kl_global_name, namespace
      )

  def get_desc(self):
    return "Mirror"

  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    undq_cpp_type_expr, dq = cpp_type_expr.get_undq()
    if dq.is_direct:
      spec = self.cpp_global_expr_to_spec.get(undq_cpp_type_expr)
      if spec:
        kl_global_name = spec.kl_global_name
        cpp_global_expr = spec.cpp_global_expr
        namespace = spec.namespace

        type_info_cache_key = kl_global_name
        type_info = self.type_info_cache.get(type_info_cache_key)
        if not type_info:
          type_info = MirrorTypeInfo(
            self.jinjenv,
            kl_global_name,
            cpp_global_expr,
            Record(
              namespace,
              include_empty_ctor=False,
              include_copy_ctor=False,
              include_simple_ass_op=False,
              include_getters_setters=False,
              include_dtor=False,
              )
            )
          self.type_info_cache.setdefault(type_info_cache_key, type_info)
          self.ext.decls.append(MirrorBuiltinDecl(self.ext, type_info))

        return DirQualTypeInfo(dq, type_info)
