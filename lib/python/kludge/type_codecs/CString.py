from kludge.type_codecs.abstract import IndRet
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

class CStringValue(CStringBase):

  @classmethod
  def maybe_get_type_codec(cls, cpp_type_expr, type_mgr):
    if cls.is_c_string(cpp_type_expr):
      return CStringValue(SimpleTypeName("String", "const char *"))

  def __init__(self, type_name):
    CStringBase.__init__(self, type_name)

  def gen_edk_ind_ret_param(self):
    return self.gen_edk_result_param()

  def gen_edk_store_result_pre(self):
    return self.gen_edk_result_name() + " = ";

  def gen_edk_store_result_post(self):
    return "";

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_edk_param_to_cpp_arg(self, param_name):
    return ""

  def gen_cpp_arg(self, param_name):
    return self.gen_get_cstring(param_name.edk)

  def gen_cpp_arg_to_edk_param(self, param_name):
    return ""

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
