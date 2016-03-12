#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import clang
from cpp_type_expr_parser import *

class Namespace:

  def __init__(self, parent_namespace, path):
    self.parent_namespace = parent_namespace
    self.path = path
    self.sub_namespaces = {}
    self.clang_type_decls = {}
    self.usings = []

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

  def maybe_find_clang_type_decl(self, child_namespace_path):
    namespace = self
    for i in range(0, len(child_namespace_path)):
      child_namespace_path_component = child_namespace_path[i]
      if i == len(child_namespace_path) - 1:
        clang_type_decl = namespace.clang_type_decls.get(child_namespace_path_component)
        if not clang_type_decl:
          for using in self.usings:
            clang_type_decl = using.clang_type_decls.get(child_namespace_path_component)
            if clang_type_decl:
              break
        if not clang_type_decl:
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
    return clang_type_decl

class NamespaceMgr:

  def __init__(self, cpp_type_expr_parser):
    # [pzion 20160311] Each member in the namespace is either a Clang cursor that is the
    # definition of the type (or typedef/using; if there is no definition, it's the declaration),
    # or a dict in the case that it's a nested namespace
    self.root_namespace = Namespace(None, [])
    self.cpp_type_expr_parser = cpp_type_expr_parser

  def _resolve_namespace(self, namespace_path):
    namespace = self.root_namespace.maybe_get_child_namespace(namespace_path)
    if not namespace:
      raise Exception("Failed to resolve namespace " + "::".join(namespace_path))
    return namespace

  def add_nested_namespace(self, namespace_path, nested_namespace_name):
    namespace = self._resolve_namespace(namespace_path)
    namespace_member = namespace.sub_namespaces.setdefault(nested_namespace_name, Namespace(namespace, namespace_path + [nested_namespace_name]))
    return namespace_path + [nested_namespace_name]

  def add_type_decl(self, namespace_path, clang_type_decl):
    namespace = self._resolve_namespace(namespace_path)
    type_name = clang_type_decl.spelling
    namespace.clang_type_decls.setdefault(type_name, clang_type_decl)
    return namespace_path + [type_name]

  def add_using_namespace(self, namespace_path, import_namespace_path):
    namespace = self._resolve_namespace(namespace_path)
    import_namespace = namespace.maybe_resolve_child_namespace(import_namespace_path)
    if not import_namespace:
      raise Exception("Failed to resolve namespace '%s' inside namespace '%s'" % ("::".join(import_namespace_path), "::".join(namespace_path)))
    namespace.usings.append(import_namespace)

  def globalize_simple_cpp_type_name(self, current_namespace_path, type_name):
    nested_type_name = type_name.split("::")
    current_namespace = self._resolve_namespace(current_namespace_path)
    while current_namespace:        
      clang_type_decl = current_namespace.maybe_find_clang_type_decl(nested_type_name)
      if clang_type_decl:
        nested_type_name = current_namespace.path + nested_type_name
        break
      current_namespace = current_namespace.parent_namespace
    return "::".join(nested_type_name)

  def globalize_cpp_type_expr(self, current_namespace_path, cpp_type_expr):
    def globalize_name(name):
      return self.globalize_simple_cpp_type_name(current_namespace_path, name)
    cpp_type_expr.tranform_names(globalize_name)

  def resolve_cpp_type_expr(self, current_namespace_path, value):
    current_namespace = self._resolve_namespace(current_namespace_path)
    if isinstance(value, clang.cindex.Type):
      type_name = value.spelling
    elif isinstance(value, basestring):
      type_name = value
    else:
      raise Exception("unexpected value type")
    cpp_type_expr = self.cpp_type_expr_parser.parse(type_name)
    self.globalize_cpp_type_expr(current_namespace_path, cpp_type_expr)
    return cpp_type_expr

