from kludge.CPPTypeExpr import ReferenceTo

def is_const_ref(cpp_type_expr):
  return isinstance(cpp_type_expr, ReferenceTo) and cpp_type_expr.pointee.is_const
