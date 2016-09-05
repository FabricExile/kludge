#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

# import clang
from cpp_type_expr_parser import *

class Namespace:

  def __init__(self, parent_namespace, cpp_type_expr):
    assert isinstance(cpp_type_expr, Named)
    self.parent_namespace = parent_namespace
    self.cpp_type_expr = cpp_type_expr
    self.sub_namespaces = {}
    self.global_cpp_type_exprs = {}
    self.usings = []

  def maybe_get_child_namespace(self, named):
    assert isinstance(named, Named)
    namespace = self
    for component in named.components:
      local_named = Named([component])
      sub_namespace = namespace.sub_namespaces.get(local_named)
      if not sub_namespace:
        for using in self.usings:
          sub_namespace = using.sub_namespaces.get(local_named)
          if sub_namespace:
            break
      if not sub_namespace:
        return None
      namespace = sub_namespace
    return namespace

  def maybe_resolve_child_namespace(self, child_namespace_path):
    namespace = self
    while namespace:
      child_namespace = namespace.maybe_get_child_namespace(child_namespace_path)
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
      named = Named([component])
      if i == len(components) - 1:
        global_cpp_type_expr = namespace.global_cpp_type_exprs.get(named)
        if not global_cpp_type_expr:
          for using in self.usings:
            global_cpp_type_expr = using.global_cpp_type_exprs.get(named)
            if global_cpp_type_expr:
              break
        if not global_cpp_type_expr:
          return None
      else:
        sub_namespace = namespace.sub_namespaces.get(named)
        if not sub_namespace:
          for using in self.usings:
            sub_namespace = using.sub_namespaces.get(named)
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
    self.root_namespace = Namespace(None, Named([]))
    self.cpp_type_expr_parser = Parser()

  def _resolve_namespace(self, namespace_path):
    namespace = self.root_namespace.maybe_get_child_namespace(namespace_path)
    if not namespace:
      raise Exception("Failed to resolve namespace " + "::".join(namespace_path))
    return namespace

  def add_namespace_alias(self, new_namespace_alias_path, old_namespace_path):
    old_namespace = self._resolve_namespace(old_namespace_path)
    new_namespace_parent = self._resolve_namespace(new_namespace_alias_path[:-1])
    new_namespace_member = new_namespace_parent.sub_namespaces.setdefault(new_namespace_alias_path[-1], old_namespace)

  def add_nested_namespace(self, namespace_path, nested_namespace_name):
    namespace = self._resolve_namespace(namespace_path)
    local_named = Named([Simple(nested_namespace_name)])
    global_named = namespace.cpp_type_expr.extension(local_named)
    nested_namespace = Namespace(namespace, global_named)
    namespace_member = namespace.sub_namespaces.setdefault(local_named, nested_namespace)
    return nested_namespace

  def add_type(self, ns_cpp_type_expr, local_cpp_type_expr, global_cpp_type_expr):
    assert isinstance(ns_cpp_type_expr, Named)
    namespace = self._resolve_namespace(ns_cpp_type_expr)
    namespace.global_cpp_type_exprs.setdefault(local_cpp_type_expr, global_cpp_type_expr)

  def add_using_namespace(self, namespace_path, import_namespace_path):
    namespace = self._resolve_namespace(namespace_path)
    import_namespace = namespace.maybe_resolve_child_namespace(import_namespace_path)
    if not import_namespace:
      raise Exception("Failed to resolve namespace '%s' inside namespace '%s'" % ("::".join(import_namespace_path), "::".join(namespace_path)))
    namespace.usings.append(import_namespace)

  def globalize_components(self, ns_cpp_type_expr, components):
    result = components
    current_namespace = self._resolve_namespace(ns_cpp_type_expr)
    while current_namespace:        
      global_cpp_type_expr = current_namespace.maybe_find_components(components)
      if global_cpp_type_expr:
        result = current_namespace.cpp_type_expr.components + components
        break
      current_namespace = current_namespace.parent_namespace
    if len(result) >= 2 \
      and isinstance(result[0], Simple) \
      and result[0].name == 'std' \
      and isinstance(result[1], Simple) \
      and result[1] == '__1':
      result = [result[0]] + result[2:]
    return result

  def globalize_cpp_type_expr(self, ns_cpp_type_expr, cpp_type_expr):
    def globalize_nested_name(nested_name):
      return self.globalize_components(ns_cpp_type_expr, nested_name)
    cpp_type_expr.tranform_names(globalize_nested_name)

  def resolve_cpp_type_expr(self, ns_cpp_type_expr, cpp_type_name):
    assert isinstance(cpp_type_name, basestring)
    current_namespace = self._resolve_namespace(ns_cpp_type_expr)
    cpp_type_expr = self.cpp_type_expr_parser.parse(cpp_type_name)
    self.globalize_cpp_type_expr(ns_cpp_type_expr, cpp_type_expr)
    return cpp_type_expr

