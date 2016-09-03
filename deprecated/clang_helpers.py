#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from clang.cindex import CursorKind, TypeKind

def compute_nested_cursor_name(clang_cursor):
  semantic_parent = clang_cursor.semantic_parent
  if semantic_parent and semantic_parent.kind in [
      CursorKind.NAMESPACE,
      CursorKind.CLASS_DECL,
      CursorKind.STRUCT_DECL,
      ]:
      result = compute_nested_cursor_name(semantic_parent)
      result.append(clang_cursor.spelling)
  else:
      result = [clang_cursor.spelling]
  return result

def compute_nested_type_name(clang_type):
  raise Exception("foo")
  print clang_type.kind
  if clang_type.kind == TypeKind.LVALUEREFERENCE:
    pointee = clang_type.get_pointee()
    result = compute_nested_type_name(pointee)
    if pointee.is_const_qualified():
      result[-1] += " const"
    result[-1] += " &"
  elif clang_type.kind == TypeKind.POINTER:
    pointee = clang_type.get_pointee()
    result = compute_nested_type_name(pointee)
    if pointee.is_const_qualified():
      result[-1] += " const"
    result[-1] += " *"
  else:
    decl_cursor = clang_type.get_declaration()
    if decl_cursor.location.file:
      return compute_nested_cursor_name(decl_cursor)
    else:
      return [clang_type.spelling]
  return result
