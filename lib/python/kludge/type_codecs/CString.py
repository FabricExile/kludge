from kludge.type_codecs.abstract import IndRet
from kludge.type_codecs.recipes import *
from kludge import CPPTypeExpr
from kludge import SimpleTypeName

class CStringBase(IndRet):

  @classmethod
  def is_c_string(cls, cpp_type_expr):
    return isinstance(cpp_type_expr, CPPTypeExpr.Pointer) \
      and cpp_type_expr.pointee.is_const \
      and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Char)

  def __init__(self, type_name):
    IndRet.__init__(self, type_name)

  def gen_get_cstring(self, edk_name):
    return edk_name + ".getCString()"

@match_cpp_expr_type(
  CPPTypeExpr.Pointer(CPPTypeExpr.Char().make_const()),
  SimpleTypeName('String', 'const char *')
  )
@indirect_result
@in_param
@cpp_arg_is_edk_param(lambda cpp_arg: cpp_arg + ".getCString()")
class CStringValue(CStringBase):

  @classmethod
  def maybe_get_type_codec(cls, cpp_type_expr, type_mgr):
    if cls.is_c_string(cpp_type_expr):
      return CStringValue(SimpleTypeName("String", "const char *"))

  def __init__(self, type_name):
    CStringBase.__init__(self, type_name)

class CStringConstRef(CStringValue):

  @classmethod
  def is_c_string_const_ref(cls, cpp_type_expr):
    return isinstance(cpp_type_expr, CPPTypeExpr.Reference) \
      and cpp_type_expr.pointee.is_const \
      and cls.is_c_string(cpp_type_expr.pointee)

  @classmethod
  def maybe_get_type_codec(cls, cpp_type_expr, type_mgr):
    if cls.is_c_string_const_ref(cpp_type_expr):
      return CStringConstRef(SimpleTypeName("String", "const char *"))

  def __init__(self, type_name):
    CStringValue.__init__(self, type_name)
