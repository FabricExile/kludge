#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

import os, jinja2
from libkludge.cpp_type_expr_parser import *
from record import Record
from alias import Alias
from enum import Enum
from func import Func
from bin_op import BinOp
from param import Param
from massage import *
from libkludge.types import KLExtTypeAliasSelector
from libkludge.types import WrappedSelector
from libkludge.types import EnumSelector
from libkludge.util import EmptyCommentContainer
from libkludge.type_simplifier import TypeSimplifier, NullTypeSimplifier

class RawTypeSimplifier(TypeSimplifier):

  def __init__(self):
    TypeSimplifier.__init__(self)

  def param_cost(self, type_info):
    return 0
    
  def param_type_name_base(self, type_info):
    return type_info.kl_for_derivatives.name.base

  def param_type_name_suffix(self, type_info):
    return type_info.kl_for_derivatives.name.suffix

  def render_param_pass_type(self, type_info):
    return "in"

  def render_param_pre(self, ti, vn):
    return ti.kl.name.compound + " __" + vn + "(" + vn + ");"

  def param_cxx_value_name(self, ti, vn):
    return "__" + vn;

  def result_type_name(self, type_info):
    return type_info.kl_for_derivatives.name

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

  def add_func(
    self,
    cpp_name,
    returns=None,
    params=[],
    opt_params=[],
    kl_name=None,
    ):
    cpp_local_name = cpp_name
    try:
      cpp_global_name = "::".join(self.nested_cpp_names + [cpp_local_name])

      kl_local_name = kl_name
      if not kl_local_name:
        kl_local_name = cpp_local_name
      kl_global_name = "_".join(self.nested_kl_names + [kl_local_name])

      returns = massage_returns(returns)
      params = massage_params(params)
      opt_params = massage_params(opt_params)

      result = None
      for i in range(0, len(opt_params)+1):
        func = Func(
          self,
          cpp_global_name,
          kl_global_name,
          returns,
          params + opt_params[0:i],
          )
        self.ext.add_decl(func)
        promotion_sig, promotion_cost = func.get_promotion_data()
        if not promotion_sig in self.ext.func_promotions \
          or self.ext.func_promotions[promotion_sig][1] > promotion_cost:
          self.ext.func_promotions[promotion_sig] = (func, promotion_cost)
        if not result:
          result = func
      return result
    except Exception as e:
      self.warning("Ignoring func %s: %s" % (cpp_local_name, e))
      return EmptyCommentContainer()

  def add_bin_op(self, op, returns, params):
    try:
      bin_op = BinOp(
        self,
        op,
        massage_returns(returns),
        massage_params(params),
        )
      self.ext.add_decl(bin_op)
      return bin_op
    except Exception as e:
      self.warning("Ignoring bin_op %s: %s" % (op, e))
      return EmptyCommentContainer()

  def add_alias(self, new_cpp_type_name, old_cpp_type_name):
    try:
      direct_new_cpp_global_expr = self.cpp_type_expr_parser.parse(new_cpp_type_name).prefix(self.components)
      direct_old_cpp_global_expr = self.resolve_cpp_type_expr(old_cpp_type_name)
      self.type_mgr.add_alias(direct_new_cpp_global_expr, direct_old_cpp_global_expr)
      direct_new_kl_local_name = new_cpp_type_name
      direct_new_kl_global_name = '_'.join(self.nested_kl_names + [direct_new_kl_local_name])
      direct_old_dqti = self.type_mgr.get_dqti(direct_old_cpp_global_expr)
      direct_alias = Alias(self, direct_new_kl_global_name, direct_old_dqti.type_info)
      self.ext.add_decl(direct_alias)

      const_ptr_new_cpp_type_expr = PointerTo(Const(direct_new_cpp_global_expr))
      const_ptr_old_cpp_type_expr = PointerTo(Const(direct_old_cpp_global_expr))
      self.type_mgr.add_alias(const_ptr_new_cpp_type_expr, const_ptr_old_cpp_type_expr)
      const_ptr_new_kl_type_name = "Cxx" + direct_new_kl_global_name + "ConstPtr"
      const_ptr_old_dqti = self.type_mgr.get_dqti(const_ptr_old_cpp_type_expr)
      const_ptr_old_kl_type_name = const_ptr_old_dqti.type_info.kl.name.compound
      const_ptr_alias = Alias(self, const_ptr_new_kl_type_name, const_ptr_old_dqti.type_info)
      self.ext.add_decl(const_ptr_alias)
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
      mutable_ptr_new_kl_type_name = "Cxx" + direct_new_kl_global_name + "Ptr"
      mutable_ptr_old_dqti = self.type_mgr.get_dqti(mutable_ptr_old_cpp_type_expr)
      mutable_ptr_old_kl_type_name = mutable_ptr_old_dqti.type_info.kl.name.compound
      mutable_ptr_alias = Alias(self, mutable_ptr_new_kl_type_name, mutable_ptr_old_dqti.type_info)
      self.ext.add_decl(mutable_ptr_alias)
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
      const_ref_new_kl_type_name = "Cxx" + direct_new_kl_global_name + "ConstRef"
      const_ref_old_dqti = self.type_mgr.get_dqti(const_ref_old_cpp_type_expr)
      const_ref_old_kl_type_name = const_ref_old_dqti.type_info.kl.name.compound
      const_ref_alias = Alias(self, const_ref_new_kl_type_name, const_ref_old_dqti.type_info)
      self.ext.add_decl(const_ref_alias)
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
      mutable_ref_new_kl_type_name = "Cxx" + direct_new_kl_global_name + "Ref"
      mutable_ref_old_dqti = self.type_mgr.get_dqti(mutable_ref_old_cpp_type_expr)
      mutable_ref_old_kl_type_name = mutable_ref_old_dqti.type_info.kl.name.compound
      mutable_ref_alias = Alias(self, mutable_ref_new_kl_type_name, mutable_ref_old_dqti.type_info)
      self.ext.add_decl(mutable_ref_alias)
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
    dont_delete=False,
    is_abstract=False,
    lookup_wrapper=None,
    include_empty_ctor=True,
    include_copy_ctor=True,
    include_simple_ass_op=True,
    include_dtor=True,
    simplifier=NullTypeSimplifier(),
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
        include_empty_ctor=include_empty_ctor,
        include_copy_ctor=include_copy_ctor,
        include_simple_ass_op=include_simple_ass_op,
        include_dtor=include_dtor,
        )
    selector = self.type_mgr.named_selectors[variant]
    selector.register(
      kl_global_name,
      kl_global_name_for_derivatives,
      cpp_global_expr,
      extends_type_info,
      record,
      forbid_copy=forbid_copy,
      dont_delete=dont_delete,
      simplifier=simplifier,
      )
    self.namespace_mgr.add_type(
      self.components,
      cpp_global_expr.components[-1],
      cpp_global_expr,
      )
    if lookup_wrapper:
      self.type_mgr.get_dqti(lookup_wrapper(cpp_global_expr))
    else:
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

  def add_opaque_type(
    self,
    cpp_type_name,
    kl_type_name=None,
    extends=None,
    ):
    cpp_local_expr = self.cpp_type_expr_parser.parse(cpp_type_name)
    kl_local_name = self.maybe_generate_kl_local_name(kl_type_name, cpp_local_expr)
    extends_type_info = None
    if extends:
      extends_cpp_type_expr = PointerTo(self.cpp_type_expr_parser.parse(extends))
      extends_dqti = self.type_mgr.maybe_get_dqti(extends_cpp_type_expr)
      if extends_dqti:
        extends_type_info = extends_dqti.type_info
    return self.add_type(
      cpp_local_expr=cpp_local_expr,
      kl_local_name=kl_local_name,
      extends_type_info=extends_type_info,
      forbid_copy=False,
      is_abstract=False,
      variant='opaque',
      lookup_wrapper=PointerTo,
      include_empty_ctor=False,
      include_copy_ctor=False,
      include_simple_ass_op=False,
      include_dtor=False,
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

    raw_cpp_local_expr = cpp_local_expr
    raw_kl_local_name = 'CxxRaw' + kl_local_name
    raw_extends_type_info = None
    if extends:
      raw_extends_cpp_type_expr = self.cpp_type_expr_parser.parse(extends)
      raw_extends_dqti = self.type_mgr.maybe_get_dqti(raw_extends_cpp_type_expr)
      if raw_extends_dqti:
        raw_extends_type_info = raw_extends_dqti.type_info
        raw_extends_cpp_global_expr = raw_extends_type_info.lib.expr

    raw = self.add_type(
      cpp_local_expr=raw_cpp_local_expr,
      kl_local_name=raw_kl_local_name,
      kl_local_name_for_derivatives=kl_local_name,
      extends_type_info=raw_extends_type_info,
      forbid_copy=True,
      dont_delete=True,
      is_abstract=is_abstract,
      variant='owned',
      simplifier=RawTypeSimplifier(),
      )
    raw_cpp_global_expr = self.type_mgr.get_dqti(raw_cpp_local_expr).type_info.lib.expr

    wrapped_cpp_local_expr = Named([Template(cpp_wrapper_name, [raw_cpp_local_expr])])
    wrapped_cpp_global_expr = Named([Template(cpp_wrapper_name, [raw_cpp_global_expr])])
    wrapped_kl_local_name = 'Wrapped' + kl_local_name
    wrapped_extends_type_info = None
    if raw_extends_type_info:
      wrapped_extends_cpp_global_expr = Named([Template(cpp_wrapper_name, [raw_extends_cpp_global_expr])])
      wrapped_extends_dqti = self.type_mgr.get_dqti(wrapped_extends_cpp_global_expr)
      wrapped_extends_type_info = wrapped_extends_dqti.type_info

    wrapped = self.add_type(
      cpp_global_expr=wrapped_cpp_global_expr,
      kl_local_name=kl_local_name,
      kl_local_name_for_derivatives=wrapped_kl_local_name,
      extends_type_info=wrapped_extends_type_info,
      forbid_copy=forbid_copy,
      variant='wrapped',
      record=raw,
      )

    wrapped.raw_type_info = self.type_mgr.maybe_get_dqti(raw_cpp_global_expr).type_info
    wrapped.wrapped_type_info = self.type_mgr.maybe_get_dqti(wrapped_cpp_global_expr).type_info

    return wrapped

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
    self.ext.add_decl(enum)
    if cpp_type_expr:
      self.namespace_mgr.add_type(
        self.components,
        cpp_type_expr.components[-1],
        cpp_type_expr,
        )
    return enum
