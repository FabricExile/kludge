from kludge import TypeCodec
from kludge import CPPTypeExpr
from kludge import SimpleTypeName

class SimpleBase(TypeCodec):

  cpp_base_type_name_to_kl_type_name = {
    "bool": "Boolean",
    "char": "SInt8",
    "int8_t": "SInt8",
    "unsigned char": "UInt8",
    "uint8_t": "UInt8",
    "short": "SInt16",
    "int16_t": "SInt16",
    "unsigned short": "UInt16",
    "uint16_t": "UInt16",
    "int": "SInt32",
    "int32_t": "SInt32",
    "unsigned int": "UInt32",
    "uint32_t": "UInt32",
    "long": "SInt32",           # Warning: Linux + OS X ONLY
    "unsigned long": "UInt32",  # Warning: Linux + OS X ONLY
    "long long": "SInt64",
    "int64_t": "SInt64",
    "unsigned long long": "UInt64",
    "uint64_t": "UInt64",
    "float": "Float32",
    "double": "Float64",
    }

  def __init__(self, type_name):
    TypeCodec.__init__(self, type_name)

  def gen_edk_param_to_cpp_arg(self, param_name):
    return ""

  def gen_cpp_arg_to_edk_param(self, param_name):
    return ""
  
class SimpleValue(SimpleBase):

  @classmethod
  def maybe_get_type_codec(cls, cpp_type_expr, type_mgr):
    if isinstance(cpp_type_expr, CPPTypeExpr.Direct):
      cpp_base_type_name = cpp_type_expr.get_unqualified_desc()
      kl_type_name = cls.cpp_base_type_name_to_kl_type_name.get(cpp_base_type_name)
      if kl_type_name:
        return SimpleValue(SimpleTypeName(kl_type_name, str(cpp_type_expr)))

  def __init__(self, type_name):
    SimpleBase.__init__(self, type_name)

  def gen_edk_dir_result_type(self):
    return self.type_name.kl.compound

  def gen_edk_ind_ret_param(self):
    return ""

  def gen_edk_store_result_pre(self):
    return self.type_name.kl.base + " " + self.gen_cpp_result_name() + self.type_name.kl.suffix + " = ";

  def gen_edk_store_result_post(self):
    return "";

  def gen_edk_return_dir_result(self):
    return "return " + self.gen_cpp_result_name() + ";"

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_cpp_arg(self, param_name):
    return param_name.edk
  
class SimpleConstRef(SimpleBase):

  @classmethod
  def maybe_get_type_codec(cls, cpp_type_expr, type_mgr):
    if isinstance(cpp_type_expr, CPPTypeExpr.Reference) \
      and cpp_type_expr.pointee.is_const \
      and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Direct):
      cpp_base_type_name = cpp_type_expr.pointee.get_unqualified_desc()
      kl_type_name = cls.cpp_base_type_name_to_kl_type_name.get(cpp_base_type_name)
      if kl_type_name:
        return SimpleConstRef(SimpleTypeName(kl_type_name, str(cpp_type_expr)))

  def __init__(self, type_name):
    SimpleBase.__init__(self, type_name)

  def gen_edk_dir_result_type(self):
    return self.type_name.kl.compound

  def gen_edk_ind_ret_param(self):
    return ""

  def gen_edk_store_result_pre(self):
    return self.type_name.kl.base + " " + self.gen_cpp_result_name() + self.type_name.kl.suffix + " = ";

  def gen_edk_store_result_post(self):
    return "";

  def gen_edk_return_dir_result(self):
    return "return " + self.gen_cpp_result_name() + ";"

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_cpp_arg(self, param_name):
    return param_name.edk
  
class SimpleConstPtr(SimpleBase):

  @classmethod
  def maybe_get_type_codec(cls, cpp_type_expr, type_mgr):
    if isinstance(cpp_type_expr, CPPTypeExpr.Pointer) \
      and cpp_type_expr.pointee.is_const \
      and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Direct):
      cpp_base_type_name = cpp_type_expr.pointee.get_unqualified_desc()
      kl_type_name = cls.cpp_base_type_name_to_kl_type_name.get(cpp_base_type_name)
      if kl_type_name:
        return SimpleConstPtr(SimpleTypeName(kl_type_name, str(cpp_type_expr)))

  def __init__(self, type_name):
    SimpleBase.__init__(self, type_name)

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_cpp_arg(self, param_name):
    return self.gen_edk_ptr_to(param_name.edk)
  
class SimpleMutableRef(SimpleBase):

  @classmethod
  def maybe_get_type_codec(cls, cpp_type_expr, type_mgr):
    if isinstance(cpp_type_expr, CPPTypeExpr.Reference) \
      and cpp_type_expr.pointee.is_mutable \
      and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Direct):
      cpp_base_type_name = cpp_type_expr.pointee.get_unqualified_desc()
      kl_type_name = cls.cpp_base_type_name_to_kl_type_name.get(cpp_base_type_name)
      if kl_type_name:
        return SimpleMutableRef(SimpleTypeName(kl_type_name, str(cpp_type_expr)))

  def __init__(self, type_name):
    SimpleBase.__init__(self, type_name)

  def gen_edk_dir_result_type(self):
    return self.type_name.kl.compound

  def gen_edk_ind_ret_param(self):
    return ""

  def gen_edk_store_result_pre(self):
    return self.type_name.kl.base + " " + self.gen_cpp_result_name() + self.type_name.kl.suffix + " = ";

  def gen_edk_store_result_post(self):
    return "";

  def gen_edk_return_dir_result(self):
    return "return " + self.gen_cpp_result_name() + ";"

  def gen_kl_param(self, kl_name):
    return self.gen_kl_io_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_io_param(edk_name)

  def gen_cpp_arg(self, param_name):
    return param_name.edk
  
class SimpleMutablePtr(SimpleBase):

  @classmethod
  def maybe_get_type_codec(cls, cpp_type_expr, type_mgr):
    if isinstance(cpp_type_expr, CPPTypeExpr.Pointer) \
      and cpp_type_expr.pointee.is_mutable \
      and isinstance(cpp_type_expr.pointee, CPPTypeExpr.Direct):
      cpp_base_type_name = cpp_type_expr.pointee.get_unqualified_desc()
      kl_type_name = cls.cpp_base_type_name_to_kl_type_name.get(cpp_base_type_name)
      if kl_type_name:
        return SimpleMutablePtr(SimpleTypeName(kl_type_name, str(cpp_type_expr)))

  def __init__(self, type_name):
    SimpleBase.__init__(self, type_name)

  def gen_kl_param(self, kl_name):
    return self.gen_kl_io_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_io_param(edk_name)

  def gen_cpp_arg(self, param_name):
    return self.gen_edk_ptr_to(param_name.edk)
