#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

# import clang
from cpp_type_expr_parser import *

class Namespace:

  def __init__(self, parent_namespace, path):
    self.parent_namespace = parent_namespace
    self.paths = [path]
    self.sub_namespaces = {}
    self.cpp_type_exprs = {}
    self.usings = []

  def add_path(self, path):
    self.paths += [path]

  def maybe_get_child_namespace(self, child_namespace_path):
    namespace = self
    for i in range(0, len(child_namespace_path)):
      child_namespace_path_component = child_namespace_path[i]
      sub_namespace = namespace.sub_namespaces.get(child_namespace_path_component)
      if not sub_namespace:
        for using in self.usings:
          sub_namespace = using.sub_namespaces.get(child_namespace_path_component)
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

  def maybe_find_cpp_type_expr(self, child_namespace_path):
    namespace = self
    for i in range(0, len(child_namespace_path)):
      child_namespace_path_component = child_namespace_path[i]
      if i == len(child_namespace_path) - 1:
        cpp_type_expr = namespace.cpp_type_exprs.get(child_namespace_path_component)
        if not cpp_type_expr:
          for using in self.usings:
            cpp_type_expr = using.cpp_type_exprs.get(child_namespace_path_component)
            if cpp_type_expr:
              break
        if not cpp_type_expr:
          return None
      else:
        sub_namespace = namespace.sub_namespaces.get(child_namespace_path_component)
        if not sub_namespace:
          for using in self.usings:
            sub_namespace = using.sub_namespaces.get(child_namespace_path_component)
            if sub_namespace:
              break
        if not sub_namespace:
          return None
        namespace = sub_namespace
    return cpp_type_expr

class NamespaceMgr:

  def __init__(self):
    # [pzion 20160311] Each member in the namespace is either a Clang cursor that is the
    # definition of the type (or typedef/using; if there is no definition, it's the declaration),
    # or a dict in the case that it's a nested namespace
    self.root_namespace = Namespace(None, [])
    def maybe_lookup_cpp_type_expr(name):
      return self.root_namespace.maybe_find_cpp_type_expr(name.split("::"))
    self.cpp_type_expr_parser = Parser(maybe_lookup_cpp_type_expr)

  def _resolve_namespace(self, namespace_path):
    namespace = self.root_namespace.maybe_get_child_namespace(namespace_path)
    if not namespace:
      raise Exception("Failed to resolve namespace " + "::".join(namespace_path))
    return namespace

  def add_namespace_alias(self, new_namespace_alias_path, old_namespace_path):
    old_namespace = self._resolve_namespace(old_namespace_path)
    old_namespace.add_path(new_namespace_alias_path)
    new_namespace_parent = self._resolve_namespace(new_namespace_alias_path[:-1])
    new_namespace_member = new_namespace_parent.sub_namespaces.setdefault(new_namespace_alias_path[-1], old_namespace)

  def add_nested_namespace(self, namespace_path, nested_namespace_name):
    namespace = self._resolve_namespace(namespace_path)
    namespace_member = namespace.sub_namespaces.setdefault(nested_namespace_name, Namespace(namespace, namespace_path + [nested_namespace_name]))
    return namespace_path + [nested_namespace_name]

  def add_type(self, namespace_path, type_name, cpp_type_expr):
    namespace = self._resolve_namespace(namespace_path)
    namespace.cpp_type_exprs.setdefault(type_name, cpp_type_expr)

  def add_using_namespace(self, namespace_path, import_namespace_path):
    namespace = self._resolve_namespace(namespace_path)
    import_namespace = namespace.maybe_resolve_child_namespace(import_namespace_path)
    if not import_namespace:
      raise Exception("Failed to resolve namespace '%s' inside namespace '%s'" % ("::".join(import_namespace_path), "::".join(namespace_path)))
    namespace.usings.append(import_namespace)

  def globalize_simple_cpp_nested_name(self, current_namespace_path, nested_name):
    result = nested_name
    current_namespace = self._resolve_namespace(current_namespace_path)
    while current_namespace:        
      cpp_type_expr = current_namespace.maybe_find_cpp_type_expr(nested_name)
      if cpp_type_expr:
        result = current_namespace.paths[0] + nested_name
        break
      current_namespace = current_namespace.parent_namespace
    if len(result) >= 2 and result[0] == 'std' and result[1] == '__1':
      result = [result[0]] + result[2:]
    return result

  def globalize_cpp_type_expr(self, current_namespace_path, cpp_type_expr):
    def globalize_nested_name(nested_name):
      return self.globalize_simple_cpp_nested_name(current_namespace_path, nested_name)
    cpp_type_expr.tranform_names(globalize_nested_name)

  def resolve_cpp_type_expr(self, current_namespace_path, value):
    current_namespace = self._resolve_namespace(current_namespace_path)
    # if isinstance(value, clang.cindex.Type):
    #   type_name = value.spelling
    # el
    if isinstance(value, basestring):
      type_name = value
    else:
      raise Exception("unexpected value type")
    cpp_type_expr = self.cpp_type_expr_parser.parse(type_name)
    self.globalize_cpp_type_expr(current_namespace_path, cpp_type_expr)
    return cpp_type_expr

