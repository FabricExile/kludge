from expr import ReferenceTo

def pointee_if_const_ref(cpp_type_expr):
  if isinstance(cpp_type_expr, ReferenceTo):
    pointee = cpp_type_expr.pointee
    if pointee.is_const:
      return pointee
