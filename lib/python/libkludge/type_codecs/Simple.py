from libkludge import TypeCodec

class SimpleBase(TypeCodec):

  cpp_type_name_to_kl_type_name = {
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
    "long long": "SInt64",
    "int64_t": "SInt64",
    "unsigned long long": "UInt64",
    "uint64_t": "UInt64",
    }
  
  def __init__(self, type_name):
    TypeCodec.__init__(self, type_name)

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return ""

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return ""
  
class SimpleValue(SimpleBase):

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

  def gen_cpp_arg(self, edk_name, cpp_name):
    return edk_name
  
class SimpleConstRef(SimpleBase):

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

  def gen_cpp_arg(self, edk_name, cpp_name):
    return edk_name
  
class SimpleConstPtr(SimpleBase):

  def __init__(self, type_name):
    SimpleBase.__init__(self, type_name)

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_cpp_arg(self, edk_name, cpp_name):
    return self.gen_edk_ptr_to(edk_name)
  
class SimpleMutableRef(SimpleBase):

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

  def gen_cpp_arg(self, edk_name, cpp_name):
    return edk_name
  
class SimpleMutablePtr(SimpleBase):

  def __init__(self, type_name):
    SimpleBase.__init__(self, type_name)

  def gen_kl_param(self, kl_name):
    return self.gen_kl_io_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_io_param(edk_name)

  def gen_cpp_arg(self, edk_name, cpp_name):
    return self.gen_edk_ptr_to(edk_name)
