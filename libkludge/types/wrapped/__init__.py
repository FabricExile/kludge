#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *
from libkludge.generate.builtin_decl import BuiltinDecl

class WrappedTypeInfo(TypeInfo):

  def __init__(
    self,
    jinjenv,
    kl_global_name,
    kl_global_name_for_derivatives,
    cpp_type_expr,
    extends,
    record,
    ):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base=kl_global_name,
      kl_name_base_for_derivatives=kl_global_name_for_derivatives,
      edk_name="Fabric_EDK_KL_" + kl_global_name,
      lib_expr=cpp_type_expr,
      extends=extends,
      record=record,
      )

  def build_codec_lookup_rules(self):
    rules = TypeInfo.build_codec_lookup_rules(self)
    rules["conv"]["*"] = "types/builtin/wrapped/conv"
    rules["result"]["*"] = "types/builtin/wrapped/result"
    rules["repr"]["*"] = "types/builtin/wrapped/repr"
    return rules

class WrappedBuiltinDecl(BuiltinDecl):

  def __init__(self, ext, type_info):
    BuiltinDecl.__init__(
      self,
      ext.root_namespace,
      desc="Wrapped %s" % (type_info),
      template_path="types/builtin/wrapped/wrapped",
      test_name="Wrapped_%s" % (type_info.kl.name),
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

class WrappedSpec(object):

  def __init__(self, kl_type_name, kl_type_name_for_derivatives, cpp_type_expr, extends, record):
    self.kl_type_name = kl_type_name
    self.kl_type_name_for_derivatives = kl_type_name_for_derivatives
    self.cpp_type_expr = cpp_type_expr
    self.extends = extends
    self.record = record

class WrappedSelector(Selector):

  should_create_ptr_ref = True

  def __init__(self, ext):
    Selector.__init__(self, ext)
    self.cpp_type_expr_to_spec = {}
    self.type_info_cache = {}

  def register(self, kl_type_name, kl_type_name_for_derivatives, cpp_type_expr, extends, record):
    self.cpp_type_expr_to_spec[cpp_type_expr] = WrappedSpec(
      kl_type_name, kl_type_name_for_derivatives, cpp_type_expr, extends, record
      )

  def get_desc(self):
    return "Wrapped"

  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    undq_cpp_type_expr, dq = cpp_type_expr.get_undq()
    if dq.is_direct:
      spec = self.cpp_type_expr_to_spec.get(undq_cpp_type_expr)
      if spec:
        assert isinstance(undq_cpp_type_expr, Named) \
          and len(undq_cpp_type_expr.components) == 1 \
          and isinstance(undq_cpp_type_expr.components[0], Template) \
          and len(undq_cpp_type_expr.components[0].params) == 1 \
          and isinstance(undq_cpp_type_expr.components[0].params[0], Named) \
          and len(undq_cpp_type_expr.components[0].params[0].components) >= 1 \
          and isinstance(undq_cpp_type_expr.components[0].params[0].components[-1], Simple)
          
        kl_type_name = spec.kl_type_name
        kl_type_name_for_derivatives = spec.kl_type_name_for_derivatives
        undq_cpp_type_expr = spec.cpp_type_expr
        extends = spec.extends
        record = spec.record

        type_info_cache_key = kl_type_name
        type_info = self.type_info_cache.get(type_info_cache_key)
        if not type_info:
          type_info = WrappedTypeInfo(
            self.jinjenv,
            kl_type_name,
            kl_type_name_for_derivatives,
            undq_cpp_type_expr,
            extends=extends,
            record=record,
            )
          self.type_info_cache.setdefault(type_info_cache_key, type_info)
          self.ext.decls.append(WrappedBuiltinDecl(self.ext, type_info))

        return DirQualTypeInfo(dq, type_info)
