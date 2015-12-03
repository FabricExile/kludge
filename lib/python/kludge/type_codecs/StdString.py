from kludge.type_codecs.abstract import IndRet
from kludge import TypeCodec
from kludge.type_codecs.recipes import *
from kludge.CPPTypeExpr import *
from kludge import SimpleTypeName

@match_cpp_expr_types(
  [
    Named("std::string"),
    ReferenceTo(Const(Named("std::string"))),
    ],
  SimpleTypeName('String', 'std::string')
  )
@indirect_result(
  post=lambda edk_name: ".c_str()"
  )
@in_param
@cpp_arg_is_edk_param(lambda cpp_arg: cpp_arg + ".getCString()")
class StdString(TypeCodec): pass

class StdStringBase(IndRet):

  @classmethod
  def is_std_string(cls, cpp_type_expr):
    return isinstance(cpp_type_expr, Named) \
      and cpp_type_expr.name == "std::string"

  def __init__(self, type_name):
    IndRet.__init__(self, type_name)

  def gen_decl_std_string(self, param_name):
    return "std::string " + param_name.cpp + "(" + param_name.edk + ".getData(), " + param_name.edk + ".getLength());"

  def gen_tmp_std_string(self, param_name):
    return "std::string(" + param_name.edk + ".getData(), " + param_name.edk + ".getLength())"

  def gen_upd_std_string(self, param_name):
    return param_name.edk + " = String(" + param_name.cpp + ".size(), " + param_name.cpp + ".data());"

class StdStringConstPtr(StdStringBase):

  @classmethod
  def is_std_string_const_ptr(cls, cpp_type_expr):
    return isinstance(cpp_type_expr, PointerTo) \
      and cpp_type_expr.pointee.is_const \
      and cls.is_std_string(cpp_type_expr.pointee)

  @classmethod
  def maybe_get_type_codec(cls, cpp_type_expr, type_mgr):
    if cls.is_std_string_const_ptr(cpp_type_expr):
      return StdStringConstPtr(SimpleTypeName("String", "const std::string *"))

  def __init__(self, type_name):
    StdStringBase.__init__(self, type_name)

  def gen_indirect_result_edk_param(self):
    return self.gen_edk_result_param()

  def gen_edk_store_result_pre(self):
    return self.gen_edk_result_name() + " = ";

  def gen_edk_store_result_post(self):
    return ".c_str()";

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_edk_param_to_cpp_arg(self, param_name):
    return self.gen_decl_std_string(param_name)

  def gen_cpp_arg(self, param_name):
    return self.gen_cpp_ptr_to(param_name.cpp)

  def gen_cpp_arg_to_edk_param(self, param_name):
    return ""

class StdStringMutableRef(StdStringBase):

  @classmethod
  def is_std_string_mutable_ref(cls, cpp_type_expr):
    return isinstance(cpp_type_expr, ReferenceTo) \
      and cpp_type_expr.pointee.is_mutable \
      and cls.is_std_string(cpp_type_expr.pointee)

  @classmethod
  def maybe_get_type_codec(cls, cpp_type_expr, type_mgr):
    if cls.is_std_string_mutable_ref(cpp_type_expr):
      return StdStringMutableRef(SimpleTypeName("String", "std::string &"))

  def __init__(self, type_name):
    StdStringBase.__init__(self, type_name)

  def gen_indirect_result_edk_param(self):
    return self.gen_edk_result_param()

  def gen_edk_store_result_pre(self):
    return self.gen_edk_result_name() + " = ";

  def gen_edk_store_result_post(self):
    return ".c_str()";

  def gen_kl_param(self, kl_name):
    return self.gen_kl_io_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_io_param(edk_name)

  def gen_edk_param_to_cpp_arg(self, param_name):
    return self.gen_decl_std_string(param_name)

  def gen_cpp_arg(self, param_name):
    return param_name.cpp

  def gen_cpp_arg_to_edk_param(self, param_name):
    return self.gen_upd_std_string(param_name)

class StdStringMutablePtr(StdStringBase):

  @classmethod
  def is_std_string_mutable_ptr(cls, cpp_type_expr):
    return isinstance(cpp_type_expr, PointerTo) \
      and cpp_type_expr.pointee.is_mutable \
      and cls.is_std_string(cpp_type_expr.pointee)

  @classmethod
  def maybe_get_type_codec(cls, cpp_type_expr, type_mgr):
    if cls.is_std_string_mutable_ptr(cpp_type_expr):
      return StdStringMutablePtr(SimpleTypeName("String", "std::string *"))

  def __init__(self, type_name):
    StdStringBase.__init__(self, type_name)

  def gen_kl_param(self, kl_name):
    return self.gen_kl_io_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_io_param(edk_name)

  def gen_edk_param_to_cpp_arg(self, param_name):
    return self.gen_decl_std_string(param_name)

  def gen_cpp_arg(self, param_name):
    return self.gen_cpp_ptr_to(param_name.cpp)

  def gen_cpp_arg_to_edk_param(self, param_name):
    return self.gen_upd_std_string(param_name)
