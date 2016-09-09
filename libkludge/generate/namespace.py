#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import os, jinja2
from libkludge.cpp_type_expr_parser import Named, Component, Simple, Template, iscomponentlist
from record import Record
from alias import Alias
from enum import Enum
from func import Func
from param import Param
from massage import *
from libkludge.types import InPlaceSelector
from libkludge.types import KLExtTypeAliasSelector
from libkludge.types import DirectSelector
from libkludge.types import WrappedSelector
from libkludge.types import EnumSelector

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
  
  def resolve_cpp_type_expr(self, cpp_type_name):
    return self.namespace_mgr.resolve_cpp_type_expr(self.components, cpp_type_name)

  def resolve_dqti(self, cpp_type_name):
    return self.type_mgr.get_dqti(self.resolve_cpp_type_expr(cpp_type_name))

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

  @property
  def cpp_type_expr_to_record(self):
    return self.ext.cpp_type_expr_to_record

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

  def add_alias(self, new_cpp_type_name, old_cpp_type_name):
    new_cpp_type_expr = self.cpp_type_expr_parser.parse(new_cpp_type_name).prefix(self.components)
    old_cpp_type_expr = self.resolve_cpp_type_expr(old_cpp_type_name)
    self.type_mgr.add_alias(new_cpp_type_expr, old_cpp_type_expr)
    new_kl_type_name = new_cpp_type_name
    old_dqti = self.type_mgr.get_dqti(old_cpp_type_expr)
    alias = Alias(self, new_kl_type_name, old_dqti.type_info)
    self.ext.decls.append(alias)
    return alias

  def add_in_place_type(
    self,
    cpp_type_name,
    kl_type_name = None,
    ):
    cpp_local_name = cpp_type_name
    cpp_type_expr = self.cpp_type_expr_parser.parse(cpp_local_name).prefix(self.components)
    kl_local_name = self.maybe_generate_kl_local_name(kl_type_name, cpp_type_expr)
    kl_global_name = '_'.join(self.nested_kl_names + [kl_local_name])
    record = Record(
      self,
      "InPlaceType",
      kl_local_name,
      child_namespace_component=cpp_type_expr.components[-1],
      )
    self.type_mgr.in_place_selector.register(kl_global_name, cpp_type_expr, record)
    self.namespace_mgr.add_type(
      self.components,
      cpp_type_expr.components[-1],
      cpp_type_expr,
      )
    self.cpp_type_expr_to_record[cpp_type_expr] = record
    self.type_mgr.get_dqti(cpp_type_expr)
    return record

  def add_direct_type(
    self,
    cpp_type_name,
    kl_type_name=None,
    extends=None,
    forbid_copy=False,
    ):
    cpp_local_name = cpp_type_name
    cpp_type_expr = self.cpp_type_expr_parser.parse(cpp_local_name).prefix(self.components)
    kl_local_name = self.maybe_generate_kl_local_name(kl_type_name, cpp_type_expr)
    kl_global_name = '_'.join(self.nested_kl_names + [kl_local_name])
    if extends:
      extends_cpp_type_expr = self.cpp_type_expr_parser.parse(extends)
      extends = self.cpp_type_expr_to_record[extends_cpp_type_expr]
    self.type_mgr.add_selector(
      DirectSelector(
        self,
        kl_global_name,
        cpp_type_expr,
        )
      )
    record = Record(
      self,
      "DirectType[extends=%s forbid_copy=%s]" % (extends, forbid_copy),
      kl_local_name,
      extends=extends,
      forbid_copy=forbid_copy,
      child_namespace_component=cpp_type_expr.components[-1],
      )
    self.ext.decls.append(record)
    self.namespace_mgr.add_type(
      self.components,
      cpp_type_expr.components[-1],
      cpp_type_expr,
      )
    self.cpp_type_expr_to_record[cpp_type_expr] = record
    return record

  def add_wrapped_type(
    self,
    cpp_type_name,
    kl_type_name = None,
    extends = None
    ):
    cpp_local_name = cpp_type_name
    cpp_type_expr = self.cpp_type_expr_parser.parse(cpp_local_name)
    assert isinstance(cpp_type_expr, Named) \
      and len(cpp_type_expr.components) == 1 \
      and isinstance(cpp_type_expr.components[0], Template) \
      and len(cpp_type_expr.components[0].params) == 1 \
      and isinstance(cpp_type_expr.components[0].params[0], Named) \
      and len(cpp_type_expr.components[0].params[0].components) >= 1 \
      and isinstance(cpp_type_expr.components[0].params[0].components[-1], Simple)
    cpp_type_expr = Named([
      Template(
        cpp_type_expr.components[0].name,
        [cpp_type_expr.components[0].params[0].prefix(self.components)],
        )
      ])
    kl_local_name = self.maybe_generate_kl_local_name(kl_type_name, cpp_type_expr)
    kl_global_name = '_'.join(self.nested_kl_names + [kl_local_name])
    if extends:
      extends_cpp_type_expr = self.cpp_type_expr_parser.parse(extends)
      extends = self.cpp_type_expr_to_record[extends_cpp_type_expr]
    self.type_mgr.add_selector(
      WrappedSelector(
        self,
        kl_global_name,
        cpp_type_expr,
        )
      )
    record = Record(
      self,
      "WrappedType[extends=%s]" % (extends),
      kl_local_name,
      self.type_mgr.get_dqti(cpp_type_expr).type_info,
      extends=extends,
      child_namespace_component=cpp_type_expr.components[0].params[0].components[-1],
      )
    self.ext.decls.append(record)
    self.namespace_mgr.add_type(
      self.components,
      cpp_type_expr.components[0].params[0].components[-1],
      cpp_type_expr,
      )
    self.cpp_type_expr_to_record[cpp_type_expr] = record
    return record

  def add_kl_ext_type_alias(
    self,
    cpp_local_name,
    kl_ext_name,
    kl_global_name,
    ):
    assert isinstance(cpp_local_name, basestring)
    cpp_type_expr = self.cpp_type_expr_parser.parse(cpp_local_name)
    assert isinstance(cpp_type_expr, Named)
    assert isinstance(kl_ext_name, basestring)
    self.ext.add_kl_require(kl_ext_name)
    assert isinstance(kl_global_name, basestring)
    self.type_mgr.add_selector(
      KLExtTypeAliasSelector(
        self,
        cpp_type_expr,
        kl_global_name,
        )
      )
    record = Record(
      self,
      "KLExtTypeAlias[ext=%s]",
      kl_global_name,
      self.type_mgr.get_dqti(cpp_type_expr).type_info,
      include_empty_ctor = False,
      include_copy_ctor = False,
      include_simple_ass_op = False,
      include_getters_setters = False,
      include_dtor = False,
      )
    self.ext.decls.append(record)
    self.namespace_mgr.add_type(
      self.components,
      cpp_type_expr.components[-1],
      cpp_type_expr,
      )
    self.cpp_type_expr_to_record[cpp_type_expr] = record
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
    if are_values_namespaced:
      child_namespace_component = cpp_type_expr.components[-1]
    else:
      child_namespace_component = None
    enum = Enum(
      self,
      kl_local_name,
      self.type_mgr.get_dqti(cpp_type_expr).type_info,
      clean_values,
      child_namespace_component=child_namespace_component,
      )
    self.ext.decls.append(enum)
    self.namespace_mgr.add_type(
      self.components,
      cpp_type_expr.components[-1],
      cpp_type_expr,
      )
    return enum
