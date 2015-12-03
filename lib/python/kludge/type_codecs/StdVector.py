from kludge.type_codecs.abstract import IndRet
from kludge import CPPTypeExpr
from kludge import TypeName

class StdVectorBase(IndRet):

  @classmethod
  def is_std_vector(cls, cpp_type_expr):
    return isinstance(cpp_type_expr, CPPTypeExpr.Template) \
      and cpp_type_expr.name == "std::vector"

  def __init__(self, type_name, element_type_codec):
    IndRet.__init__(self, type_name)
    self._element_type_codec = element_type_codec

  def gen_decl_std_vector(self, edk_name, cpp_name):
    element_edk_name = edk_name + "[i]"
    element_cpp_name = "element"
    return """std::vector< %s > %s;
for ( uint32_t i = 0; i < %s.size(); ++i )
{
  %s
  %s.push_back(%s);
}""" % (
  self._element_type_codec.type_name.cpp,
  cpp_name,
  edk_name,
  self._element_type_codec.gen_edk_param_to_cpp_arg(element_edk_name, element_cpp_name),
  cpp_name,
  self._element_type_codec.gen_cpp_arg(element_edk_name, element_cpp_name),
  )

  def gen_upd_std_string(self, edk_name, cpp_name):
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

  def gen_edk_ind_ret_param(self):
    return self.gen_edk_result_param()

  def gen_edk_store_result_pre(self):
    raise Exception("Unimplemented")

  def gen_edk_store_result_post(self):
    raise Exception("Unimplemented")

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return self.gen_decl_std_vector(edk_name, cpp_name)

  def gen_cpp_arg(self, edk_name, cpp_name):
    return cpp_name

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
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
