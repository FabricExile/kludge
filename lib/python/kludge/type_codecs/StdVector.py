from kludge.type_codecs.abstract import IndRet
from kludge import CPPTypeExpr
from kludge import ParamName
from kludge import TypeName

class StdVectorBase(IndRet):

  @classmethod
  def is_std_vector(cls, cpp_type_expr):
    return isinstance(cpp_type_expr, CPPTypeExpr.Template) \
      and cpp_type_expr.name == "std::vector"

  def __init__(self, type_name, element_type_codec):
    IndRet.__init__(self, type_name)
    self._element_type_codec = element_type_codec

  def gen_decl_std_vector(self, param_name):
    element_param = ParamName("RESERVED_element")
    element_param.edk = param_name.edk + "[i]"
    return """std::vector< %s > %s;
for ( uint32_t i = 0; i < %s.size(); ++i )
{
  %s
  %s.push_back(%s);
}""" % (
  self._element_type_codec.type_name.cpp,
  param_name.cpp,
  param_name.edk,
  self._element_type_codec.gen_edk_param_to_cpp_arg(element_param),
  param_name.cpp,
  self._element_type_codec.gen_cpp_arg(element_param),
  )

  def gen_upd_std_string(self, param_name):
    raise Exception("Unimplemented")

class StdVectorValue(StdVectorBase):

  @classmethod
  def maybe_get_type_codec(cls, cpp_type_expr, type_mgr):
    if cls.is_std_vector(cpp_type_expr):
      element_type_codec = type_mgr.get_type_codec(str(cpp_type_expr.params[0]))
      return StdVectorValue(
        TypeName(
          element_type_codec.type_name.kl.base,
          element_type_codec.type_name.kl.suffix + "[]",
          "VariableArray< " + element_type_codec.type_name.edk + " >",
          "std::vector< " + element_type_codec.type_name.cpp + " >",
          ),
        element_type_codec
        )

  def __init__(self, type_name, element_type_codec):
    StdVectorBase.__init__(self, type_name, element_type_codec)

  def gen_indirect_result_edk_param(self):
    return self.gen_edk_result_param()

  def gen_edk_store_result_pre(self):
    raise Exception("Unimplemented")

  def gen_edk_store_result_post(self):
    raise Exception("Unimplemented")

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_edk_param_to_cpp_arg(self, param_name):
    return self.gen_decl_std_vector(param_name)

  def gen_cpp_arg(self, param_name):
    return param_name.cpp

  def gen_cpp_arg_to_edk_param(self, param_name):
    return ""

class StdVectorConstRef(StdVectorValue):

  @classmethod
  def is_std_vector_const_ref(cls, cpp_type_expr):
    return isinstance(cpp_type_expr, CPPTypeExpr.Reference) \
      and cpp_type_expr.pointee.is_const \
      and cls.is_std_vector(cpp_type_expr.pointee)

  @classmethod
  def maybe_get_type_codec(cls, cpp_type_expr, type_mgr):
    if cls.is_std_vector_const_ref(cpp_type_expr):
      element_type_codec = type_mgr.get_type_codec(str(cpp_type_expr.pointee.params[0]))
      return StdVectorConstRef(
        TypeName(
          element_type_codec.type_name.kl.base,
          element_type_codec.type_name.kl.suffix + "[]",
          "VariableArray< " + element_type_codec.type_name.edk + " >",
          "const std::vector< " + element_type_codec.type_name.cpp + " > &",
          ),
        element_type_codec
        )

  def __init__(self, type_name, element_type_codec):
    StdVectorValue.__init__(self, type_name, element_type_codec)
