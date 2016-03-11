#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import clang

class Namespace:

  def __init__(self, parent_namespace, path):
    self.parent_namespace = parent_namespace
    self.path = path
    self.elements = {}

  def maybe_find_clang_type_decl(self, child_namespace_element_path):
    first_namespace_element = self.elements.get(child_namespace_element_path[0])
    if not first_namespace_element:
      return None
    elif len(child_namespace_element_path) > 1:
      if not isinstance(first_namespace_element, dict):
        return None
      return first_namespace_element.maybe_find_clang_type_decl(child_namespace_element_path[1:])
    else:
      if isinstance(first_namespace_element, dict):
        return None
      return first_namespace_element

class NamespaceMgr:

  base_types = [
    "char",
    "signed char",
    "unsigned char",
    "int",
    "signed int",
    "unsigned int",
    "short",
    "signed short",
    "unsigned short",
    "long",
    "signed long",
    "unsigned long",
    "long long",
    "signed long long",
    "unsigned long long",
    "signed",
    "unsigned",
    "float",
    "double",
    "size_t",
    "int8_t",
    "uint8_t",
    "int16_t",
    "uint16_t",
    "int32_t",
    "uint32_t",
    "int64_t",
    "uint64_t",
    ]

  def __init__(self):
    # [pzion 20160311] Each element in the namespace is either a Clang cursor that is the
    # definition of the type (or typedef/using; if there is no definition, it's the declaration),
    # or a dict in the case that it's a nested namespace
    self.root_namespace = Namespace(None, [])

  def _resolve_namespace_dict(self, namespace_path):
    namespace_dict = self.root_namespace
    for i in range(0, len(namespace_path)):
      namespace_value = namespace_dict.elements.get(namespace_path[i])
      if not namespace_value:
        raise Exception(
          "Unable to resolve namespace '%s'" % "::".join(namespace_path[0:i+1])
          )
      elif isinstance(namespace_value, dict):
        namespace_dict = namespace_value
      else:
        raise Exception(
          "Namespace element '%s' is not a nested namespace" % "::".join(namespace_path[0:i+1])
          )
    return namespace_dict

  def add_nested_namespace(self, parent_namespace_path, nested_namespace_name):
    namespace_dict = self._resolve_namespace_dict(namespace_path)
    namespace_element = namespace_dict.elements.setdefault(nested_namespace_name, {})
    if not isinstance(namespace_element, dict):
      raise Exception(
        "Existing namespace element '%s' is not a nested namespace" % "::".join(namespace_path[0:i+1])
        )

  def add_type_decl(self, namespace_path, clang_type_decl_cursor):
    namespace_dict = self._resolve_namespace_dict(namespace_path)
    type_name = clang_type_decl_cursor.spelling
    print "add_type_decl: type_name=%s" % type_name
    existing_namespace_element = namespace_dict.elements.get(type_name)
    if existing_namespace_element:
      pass # do something here to upgrade declarations to definitions
    namespace_dict.set(type_name, clang_type_decl_cursor)

  def get_nested_type_name(self, current_namespace_path, value):
    current_namespace = self._resolve_namespace_dict(current_namespace_path)
    if isinstance(value, clang.cindex.Type):
      type_name = value.spelling
    elif isinstance(value, basestring):
      type_name = value
    else:
      raise Exception("unexpected value type")
    if type_name in self.base_types:
      return [type_name]
    type_name = type_name.split("::")
    while current_namespace:        
      clang_type_decl = current_namespace.maybe_find_clang_type_decl(type_name)
      if clang_type_decl:
        return current_namespace.path + type_name
      current_namespace = current_namespace.parent_namespace
    return type_name
