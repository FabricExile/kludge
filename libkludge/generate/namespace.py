#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import os, jinja2
from libkludge.cpp_type_expr_parser import *
from record import Record
from alias import Alias
from enum import Enum
from func import Func
from param import Param
from massage import *
from libkludge.types import KLExtTypeAliasSelector
from libkludge.types import WrappedSelector
from libkludge.types import EnumSelector
from libkludge.util import EmptyCommentContainer

class Namespace:

  def __init__(
    self,
    ext,
    parent_namespace,
    components,
    kl_name,
    ):
    self.ext = ext
    self.parent_namespace = parent_namespace
    assert iscomponentlist(components)
    self.components = components
    if parent_namespace:
      assert isinstance(kl_name, basestring)
      assert components[:-1] == parent_namespace.components
      self.nested_kl_names = parent_namespace.nested_kl_names + [kl_name]
    else:
      self.nested_kl_names = []

    for method_name in [
      'error',
      'warning',
      'info',
      'debug',
      ]:
      setattr(self, method_name, getattr(ext, method_name))

  @property
  def nested_cpp_names(self):
    return [str(component) for component in self.components]
  
  def create_child(self, component, kl_name):
    assert isinstance(component, Component)
    assert isinstance(kl_name, basestring)
    nested_namespace = self.namespace_mgr.add_nested_namespace(self.components, component)
    return Namespace(self.ext, self, nested_namespace.components, kl_name)

  def resolve_dqti(self, cpp_type_name):
    result = self.namespace_mgr.resolve_dqti(self.components, cpp_type_name)
    if not result:
      raise Exception("unable to resolve type '%s' in namespace '%s'" % (
        cpp_type_name,
        '::'.join([component.get_desc() for component in self.components]),
        ))
    return result
  
  def resolve_cpp_type_expr(self, cpp_type_name):
    dqti = self.resolve_dqti(cpp_type_name)
    if dqti:
      return dqti.type_info.lib.expr

  @property
  def cpp_type_expr_parser(self):
    return self.ext.cpp_type_expr_parser

  @property
  def type_mgr(self):
    return self.ext.type_mgr

  @property
  def namespace_mgr(self):
    return self.ext.namespace_mgr

  @property
  def jinjenv(self):
    return self.ext.jinjenv

  def maybe_generate_kl_local_name(self, kl_local_name, cpp_type_expr):
    if not kl_local_name:
      assert isinstance(cpp_type_expr, Named)
      if isinstance(cpp_type_expr.components[-1], Simple):
        kl_local_name = cpp_type_expr.components[-1].name
      elif isinstance(cpp_type_expr.components[-1], Template) \
        and len(cpp_type_expr.components[-1].params) == 1 \
        and isinstance(cpp_type_expr.components[-1].params[0], Named) \
        and isinstance(cpp_type_expr.components[-1].params[0].components[-1], Simple):
        kl_local_name = cpp_type_expr.components[-1].params[0].components[-1].name
      else:
        raise Exception(str(cpp_type_expr) + ": unable to generate kl_local_name")
    return kl_local_name

  def add_namespace(self, cpp_name, kl_name=None):
    if not kl_name:
      kl_name = cpp_name
    cpp_type_expr = self.cpp_type_expr_parser.parse(cpp_name)
    assert len(cpp_type_expr.components) == 1 \
      and isinstance(cpp_type_expr.components[0], Simple)
    return self.create_child(cpp_type_expr.components[0], kl_name)

  def add_func(self, cpp_name, returns=None, params=[], kl_name=None):
    cpp_local_name = cpp_name
    try:
      cpp_global_name = "::".join(self.nested_cpp_names + [cpp_local_name])

      kl_local_name = kl_name
      if not kl_local_name:
        kl_local_name = cpp_local_name
      kl_global_name = "_".join(self.nested_kl_names + [kl_local_name])

      func = Func(
        self,
        cpp_global_name,
        kl_global_name,
        massage_returns(returns),
        massage_params(params),
        )
      self.ext.decls.append(func)
      return func
    except Exception as e:
      self.warning("Ignoring function %s: %s" % (cpp_local_name, e))
      return EmptyCommentContainer()

  def add_alias(self, new_cpp_type_name, old_cpp_type_name):
    try:
      direct_new_cpp_global_expr = self.cpp_type_expr_parser.parse(new_cpp_type_name).prefix(self.components)
      direct_old_cpp_global_expr = self.resolve_cpp_type_expr(old_cpp_type_name)
      self.type_mgr.add_alias(direct_new_cpp_global_expr, direct_old_cpp_global_expr)
      direct_new_kl_local_name = new_cpp_type_name
      direct_new_kl_global_name = '_'.join(self.nested_kl_names + [direct_new_kl_local_name])
      direct_old_dqti = self.type_mgr.get_dqti(direct_old_cpp_global_expr)
      print "direct_old_dqti.type_info.kl.name = " + str(direct_old_dqti.type_info.kl.name)
      print "direct_old_dqti.type_info.edk.name = " + str(direct_old_dqti.type_info.edk.name)
      print "direct_old_dqti.type_info.lib.name = " + str(direct_old_dqti.type_info.lib.name)
      print "direct_old_dqti.type_info.lib.expr = " + str(direct_old_dqti.type_info.lib.expr)
      direct_alias = Alias(self, direct_new_kl_global_name, direct_old_dqti.type_info)
      self.ext.decls.append(direct_alias)

      const_ptr_new_cpp_type_expr = PointerTo(Const(direct_new_cpp_global_expr))
      const_ptr_old_cpp_type_expr = PointerTo(Const(direct_old_cpp_global_expr))
      self.type_mgr.add_alias(const_ptr_new_cpp_type_expr, const_ptr_old_cpp_type_expr)
      const_ptr_new_kl_type_name = direct_new_kl_global_name + "_CxxConstPtr"
      const_ptr_old_dqti = self.type_mgr.get_dqti(const_ptr_old_cpp_type_expr)
      const_ptr_old_kl_type_name = const_ptr_old_dqti.type_info.kl.name.compound
      const_ptr_alias = Alias(self, const_ptr_new_kl_type_name, const_ptr_old_dqti.type_info)
      self.ext.decls.append(const_ptr_alias)
      self.ext.add_kl_epilog("""
%s Make_%s(%s value) {
  return Make_%s(value);
}

%s Make_%s(io %s value) {
  return Make_%s(value);
}
""" % (
        const_ptr_new_kl_type_name,
        const_ptr_new_kl_type_name,
        direct_new_kl_global_name,
        const_ptr_old_kl_type_name,
        const_ptr_new_kl_type_name,
        const_ptr_new_kl_type_name,
        direct_new_kl_global_name,
        const_ptr_old_kl_type_name,
        ));

      mutable_ptr_new_cpp_type_expr = PointerTo(direct_new_cpp_global_expr)
      mutable_ptr_old_cpp_type_expr = PointerTo(direct_old_cpp_global_expr)
      self.type_mgr.add_alias(mutable_ptr_new_cpp_type_expr, mutable_ptr_old_cpp_type_expr)
      mutable_ptr_new_kl_type_name = direct_new_kl_global_name + "_CxxPtr"
      mutable_ptr_old_dqti = self.type_mgr.get_dqti(mutable_ptr_old_cpp_type_expr)
      mutable_ptr_old_kl_type_name = mutable_ptr_old_dqti.type_info.kl.name.compound
      mutable_ptr_alias = Alias(self, mutable_ptr_new_kl_type_name, mutable_ptr_old_dqti.type_info)
      self.ext.decls.append(mutable_ptr_alias)
      self.ext.add_kl_epilog("""
%s Make_%s(%s value) {
  return Make_%s(value);
}

%s Make_%s(io %s value) {
  return Make_%s(value);
}
""" % (
        mutable_ptr_new_kl_type_name,
        mutable_ptr_new_kl_type_name,
        direct_new_kl_global_name,
        mutable_ptr_old_kl_type_name,
        mutable_ptr_new_kl_type_name,
        mutable_ptr_new_kl_type_name,
        direct_new_kl_global_name,
        mutable_ptr_old_kl_type_name,
        ));

      const_ref_new_cpp_type_expr = ReferenceTo(Const(direct_new_cpp_global_expr))
      const_ref_old_cpp_type_expr = ReferenceTo(Const(direct_old_cpp_global_expr))
      self.type_mgr.add_alias(const_ref_new_cpp_type_expr, const_ref_old_cpp_type_expr)
      const_ref_new_kl_type_name = direct_new_kl_global_name + "_CxxConstRef"
      const_ref_old_dqti = self.type_mgr.get_dqti(const_ref_old_cpp_type_expr)
      const_ref_old_kl_type_name = const_ref_old_dqti.type_info.kl.name.compound
      const_ref_alias = Alias(self, const_ref_new_kl_type_name, const_ref_old_dqti.type_info)
      self.ext.decls.append(const_ref_alias)
      self.ext.add_kl_epilog("""
%s Make_%s(%s value) {
  return Make_%s(value);
}

%s Make_%s(io %s value) {
  return Make_%s(value);
}
""" % (
        const_ref_new_kl_type_name,
        const_ref_new_kl_type_name,
        direct_new_kl_global_name,
        const_ref_old_kl_type_name,
        const_ref_new_kl_type_name,
        const_ref_new_kl_type_name,
        direct_new_kl_global_name,
        const_ref_old_kl_type_name,
        ));

      mutable_ref_new_cpp_type_expr = ReferenceTo(direct_new_cpp_global_expr)
      mutable_ref_old_cpp_type_expr = ReferenceTo(direct_old_cpp_global_expr)
      self.type_mgr.add_alias(mutable_ref_new_cpp_type_expr, mutable_ref_old_cpp_type_expr)
      mutable_ref_new_kl_type_name = direct_new_kl_global_name + "_CxxRef"
      mutable_ref_old_dqti = self.type_mgr.get_dqti(mutable_ref_old_cpp_type_expr)
      mutable_ref_old_kl_type_name = mutable_ref_old_dqti.type_info.kl.name.compound
      mutable_ref_alias = Alias(self, mutable_ref_new_kl_type_name, mutable_ref_old_dqti.type_info)
      self.ext.decls.append(mutable_ref_alias)
      self.ext.add_kl_epilog("""
%s Make_%s(%s value) {
  return Make_%s(value);
}

%s Make_%s(io %s value) {
  return Make_%s(value);
}
""" % (
        mutable_ref_new_kl_type_name,
        mutable_ref_new_kl_type_name,
        direct_new_kl_global_name,
        mutable_ref_old_kl_type_name,
        mutable_ref_new_kl_type_name,
        mutable_ref_new_kl_type_name,
        direct_new_kl_global_name,
        mutable_ref_old_kl_type_name,
        ));

      return direct_alias
    except Exception as e:
      self.ext.warning("Ignoring alias '%s': %s" % (new_cpp_type_name, e))
      return EmptyCommentContainer()
      
  def generate_type(self, cpp_local_name):
    cpp_local_expr = self.cpp_type_expr_parser.parse(cpp_local_name)
    self.type_mgr.get_dqti(cpp_local_expr)

  def add_type(
    self,
    cpp_local_expr=None,
    cpp_global_expr=None,
    kl_local_name=None,
    kl_local_name_for_derivatives=None,
    extends_type_info=None,
    variant='owned',
    record=None,
    forbid_copy=False,
    is_abstract=False,
    ):
    if not cpp_global_expr:
      assert isinstance(cpp_local_expr, Named)
      cpp_global_expr = cpp_local_expr.prefix(self.components)
    assert isinstance(cpp_global_expr, Named)

    assert isinstance(kl_local_name, basestring)
    kl_global_name = '_'.join(self.nested_kl_names + [kl_local_name])
    if not kl_local_name_for_derivatives:
      kl_local_name_for_derivatives = kl_local_name
    kl_global_name_for_derivatives = '_'.join(self.nested_kl_names + [kl_local_name_for_derivatives])
    if not record:
      record = Record(
        self,
        child_namespace_component=cpp_global_expr.components[-1],
        child_namespace_kl_name=kl_local_name_for_derivatives,
        extends=(extends_type_info and extends_type_info.record),
        is_abstract=is_abstract,
        )
    selector = self.type_mgr.named_selectors[variant]
    selector.register(
      kl_global_name,
      kl_global_name_for_derivatives,
      cpp_global_expr,
      extends_type_info,
      record,
      forbid_copy=forbid_copy,
      )
    self.namespace_mgr.add_type(
      self.components,
      cpp_global_expr.components[-1],
      cpp_global_expr,
      )
    self.type_mgr.get_dqti(cpp_global_expr)
    return record

  def add_owned_type(
    self,
    cpp_type_name,
    kl_type_name=None,
    extends=None,
    forbid_copy=False,
    is_abstract=False,
    ):
    cpp_local_expr = self.cpp_type_expr_parser.parse(cpp_type_name)
    kl_local_name = self.maybe_generate_kl_local_name(kl_type_name, cpp_local_expr)
    extends_type_info = None
    if extends:
      extends_cpp_type_expr = self.cpp_type_expr_parser.parse(extends)
      extends_dqti = self.type_mgr.maybe_get_dqti(extends_cpp_type_expr)
      if extends_dqti:
        extends_type_info = extends_dqti.type_info
    return self.add_type(
      cpp_local_expr=cpp_local_expr,
      kl_local_name=kl_local_name,
      extends_type_info=extends_type_info,
      forbid_copy=forbid_copy,
      is_abstract=is_abstract,
      variant='owned',
      )

  def add_in_place_type(
    self,
    cpp_type_name,
    kl_type_name=None,
    extends=None,
    forbid_copy=False,
    is_abstract=False,
    ):
    cpp_local_expr = self.cpp_type_expr_parser.parse(cpp_type_name)
    kl_local_name = self.maybe_generate_kl_local_name(kl_type_name, cpp_local_expr)
    extends_type_info = None
    if extends:
      extends_cpp_type_expr = self.cpp_type_expr_parser.parse(extends)
      extends_dqti = self.type_mgr.maybe_get_dqti(extends_cpp_type_expr)
      if extends_dqti:
        extends_type_info = extends_dqti.type_info
    return self.add_type(
      cpp_local_expr=cpp_local_expr,
      kl_local_name=kl_local_name,
      extends_type_info=extends_type_info,
      forbid_copy=forbid_copy,
      is_abstract=is_abstract,
      variant='in_place',
      )

  def add_wrapped_type(
    self,
    cpp_wrapper_name,
    cpp_type_name,
    kl_type_name=None,
    extends=None,
    forbid_copy=False,
    is_abstract=False,
    ):
    cpp_local_expr = self.cpp_type_expr_parser.parse(cpp_type_name)
    kl_local_name = self.maybe_generate_kl_local_name(kl_type_name, cpp_local_expr)

    owned_cpp_local_expr = cpp_local_expr
    owned_kl_local_name = 'Raw_' + kl_local_name
    owned_extends_type_info = None
    if extends:
      owned_extends_cpp_type_expr = self.cpp_type_expr_parser.parse(extends)
      owned_extends_dqti = self.type_mgr.maybe_get_dqti(owned_extends_cpp_type_expr)
      if owned_extends_dqti:
        owned_extends_type_info = owned_extends_dqti.type_info
        owned_extends_cpp_global_expr = owned_extends_type_info.lib.expr
    owned = self.add_type(
      cpp_local_expr=owned_cpp_local_expr,
      kl_local_name=owned_kl_local_name,
      kl_local_name_for_derivatives=kl_local_name,
      extends_type_info=owned_extends_type_info,
      forbid_copy=True,
      is_abstract=is_abstract,
      variant='owned',
      )
    owned_cpp_global_expr = self.type_mgr.get_dqti(owned_cpp_local_expr).type_info.lib.expr

    wrapped_cpp_global_expr = Named([Template(cpp_wrapper_name, [owned_cpp_global_expr])])
    wrapped_kl_local_name = 'Wrapped_' + kl_local_name
    wrapped_extends_type_info = None
    if owned_extends_type_info:
      wrapped_extends_cpp_global_expr = Named([Template(cpp_wrapper_name, [owned_extends_cpp_global_expr])])
      wrapped_extends_dqti = self.type_mgr.get_dqti(wrapped_extends_cpp_global_expr)
      wrapped_extends_type_info = wrapped_extends_dqti.type_info
    return self.add_type(
      cpp_global_expr=wrapped_cpp_global_expr,
      kl_local_name=kl_local_name,
      kl_local_name_for_derivatives=wrapped_kl_local_name,
      extends_type_info=wrapped_extends_type_info,
      forbid_copy=forbid_copy,
      variant='wrapped',
      record=owned,
      )

  def add_mirror(
    self,
    cpp_local_name,
    existing_kl_global_name,
    kl_ext_name=None,
    ):
    assert isinstance(cpp_local_name, basestring)
    cpp_global_expr = self.cpp_type_expr_parser.parse(cpp_local_name)
    assert isinstance(cpp_global_expr, Named)
    kl_local_name = self.maybe_generate_kl_local_name(None, cpp_global_expr)
    kl_global_name = '_'.join(self.nested_kl_names + [kl_local_name])
    assert isinstance(existing_kl_global_name, basestring)
    self.type_mgr.named_selectors['mirror'].register(
      cpp_global_expr,
      kl_global_name,
      existing_kl_global_name,
      kl_ext_name,
      self,
      )
    self.namespace_mgr.add_type(
      self.components,
      cpp_global_expr.components[-1],
      cpp_global_expr,
      )
    record = self.type_mgr.get_dqti(cpp_global_expr).type_info.record
    return record

  def add_enum(
    self,
    cpp_local_name,
    values,
    kl_local_name = None,
    are_values_namespaced = False,
    ):
    assert isinstance(cpp_local_name, basestring)
    cur_value = 0
    clean_values = []
    for value in values:
      if isinstance(value, basestring):
        clean_values.append((value, cur_value))
      else:
        clean_values.append(value)
        cur_value = value[1]
      cur_value += 1
    if cpp_local_name:
      cpp_type_expr = self.cpp_type_expr_parser.parse(cpp_local_name).prefix(self.components)
      assert isinstance(cpp_type_expr, Named)
      assert isinstance(cpp_type_expr.components[-1], Simple)
      kl_local_name = self.maybe_generate_kl_local_name(kl_local_name, cpp_type_expr)
      kl_global_name = '_'.join(self.nested_kl_names + [kl_local_name])
      self.type_mgr.add_selector(
        EnumSelector(
          self,
          cpp_type_expr,
          kl_global_name,
          )
        )
    else:
      cpp_type_expr = None
      kl_local_name = None
    if are_values_namespaced:
      child_namespace_component = cpp_type_expr.components[-1]
    else:
      child_namespace_component = None
    enum = Enum(
      self,
      kl_local_name,
      cpp_type_expr and self.type_mgr.get_dqti(cpp_type_expr).type_info,
      clean_values,
      child_namespace_component=child_namespace_component,
      )
    self.ext.decls.append(enum)
    if cpp_type_expr:
      self.namespace_mgr.add_type(
        self.components,
        cpp_type_expr.components[-1],
        cpp_type_expr,
        )
    return enum
