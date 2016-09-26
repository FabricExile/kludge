#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

# import clang
from cpp_type_expr_parser import *

class Namespace:

  def __init__(self, parent_namespace=None, component=None):
    assert parent_namespace is None or isinstance(parent_namespace, Namespace)
    self.parent_namespace = parent_namespace
    if parent_namespace:
      assert isinstance(component, Component)
      self.components = parent_namespace.components + [component]
    else:
      assert component is None
      self.components = []
    self.sub_namespaces = {} # maps Component to Namespace
    self.global_cpp_type_exprs = {} # maps Component to CPPTypeExpr
    self.usings = []

  def maybe_get_child_namespace(self, components):
    namespace = self
    for component in components:
      sub_namespace = namespace.sub_namespaces.get(component)
      if not sub_namespace:
        for using in self.usings:
          sub_namespace = using.sub_namespaces.get(component)
          if sub_namespace:
            break
      if not sub_namespace:
        return None
      namespace = sub_namespace
    return namespace

  def maybe_resolve_child_namespace(self, components):
    namespace = self
    while namespace:
      child_namespace = namespace.maybe_get_child_namespace(components)
      if child_namespace:
        return child_namespace
      namespace = namespace.parent_namespace
    return None

  def maybe_find_components(self, components):
    assert isinstance(components, list)
    namespace = self
    for i in range(0, len(components)):
      component = components[i]
      assert isinstance(component, Component)
      if i == len(components) - 1:
        global_cpp_type_expr = namespace.global_cpp_type_exprs.get(component)
        if not global_cpp_type_expr:
          for using in self.usings:
            global_cpp_type_expr = using.global_cpp_type_exprs.get(component)
            if global_cpp_type_expr:
              break
        if not global_cpp_type_expr:
          return None
      else:
        sub_namespace = namespace.sub_namespaces.get(component)
        if not sub_namespace:
          for using in self.usings:
            sub_namespace = using.sub_namespaces.get(component)
            if sub_namespace:
              break
        if not sub_namespace:
          return None
        namespace = sub_namespace
    return global_cpp_type_expr

class NamespaceMgr:

  def __init__(self):
    # [pzion 20160311] Each member in the namespace is either a Clang cursor that is the
    # definition of the type (or typedef/using; if there is no definition, it's the declaration),
    # or a dict in the case that it's a nested namespace
    self.root_namespace = Namespace()
    self.cpp_type_expr_parser = Parser()

  def _resolve_namespace(self, components):
    namespace = self.root_namespace.maybe_get_child_namespace(components)
    if not namespace:
      raise Exception("Failed to resolve namespace " + "::".join([str(component) for component in components]))
    return namespace

  def add_namespace_alias(self, path_components, old_cpp_type_expr):
    old_namespace = self._resolve_namespace(old_cpp_type_expr)
    new_namespace_parent = self._resolve_namespace(path_components[:-1])
    new_namespace_member = new_namespace_parent.sub_namespaces.setdefault(path_components[-1], old_namespace)

  def add_nested_namespace(self, path_components, component):
    path_namespace = self._resolve_namespace(path_components)
    nested_namespace = Namespace(path_namespace, component)
    namespace_member = path_namespace.sub_namespaces.setdefault(component, nested_namespace)
    return nested_namespace

  def add_type(self, path_components, component, global_cpp_type_expr):
    assert iscomponentlist(path_components)
    assert isinstance(component, Component)
    assert isinstance(global_cpp_type_expr, Type)
    path_namespace = self._resolve_namespace(path_components)
    path_namespace.global_cpp_type_exprs.setdefault(component, global_cpp_type_expr)

  def add_using_namespace(self, path_components, import_components):
    path_namespace = self._resolve_namespace(path_components)
    import_namespace = path_namespace.maybe_resolve_child_namespace(import_components)
    if not import_namespace:
      raise Exception("Failed to resolve namespace '%s' inside namespace '%s'" % ("::".join(import_namespace_path), "::".join(namespace_path)))
    path_namespace.usings.append(import_namespace)

  def globalize_components(self, path_components, components):
    cur_namespace = self._resolve_namespace(path_components)
    while cur_namespace:        
      global_cpp_type_expr = cur_namespace.maybe_find_components(components)
      if global_cpp_type_expr:
        return cur_namespace.components + components
      cur_namespace = cur_namespace.parent_namespace
    return components

  def globalize_cpp_type_expr(self, path_components, cpp_type_expr):
    def globalize_nested_name(nested_name):
      return self.globalize_components(path_components, nested_name)
    cpp_type_expr.tranform_names(globalize_nested_name)

  def resolve_cpp_type_expr(self, path_components, cpp_type_name):
    assert isinstance(cpp_type_name, basestring)
    cpp_type_expr = self.cpp_type_expr_parser.parse(cpp_type_name)
    self.globalize_cpp_type_expr(path_components, cpp_type_expr)
    return cpp_type_expr
