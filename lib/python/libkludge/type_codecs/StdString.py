from libkludge.type_codecs.abstract import IndRet

class StdStringBase(IndRet):

  def __init__(self, kl_type_name, cpp_type_name):
    IndRet.__init__(self, kl_type_name, cpp_type_name)

  def gen_decl_std_string(self, edk_name, cpp_name):
    return "std::string " + cpp_name + "(" + edk_name + ".getData(), " + edk_name + ".getLength());"

  def gen_tmp_std_string(self, edk_name):
    return "std::string(" + edk_name + ".getData(), " + edk_name + ".getLength())"

  def gen_upd_std_string(self, edk_name, cpp_name):
    return edk_name + " = String(" + cpp_name + ".size(), " + cpp_name + ".data());"

class StdStringValue(StdStringBase):

  def __init__(self, kl_type_name, cpp_type_name):
    StdStringBase.__init__(self, kl_type_name, cpp_type_name)

  def gen_edk_ind_ret_param(self):
    return self.gen_edk_result_param()

  def gen_edk_store_result_pre(self):
    return self.gen_edk_result_name() + " = ";

  def gen_edk_store_result_post(self):
    return ".c_str()";

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return ""

  def gen_cpp_arg(self, edk_name, cpp_name):
    return self.gen_tmp_std_string(edk_name)

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return ""

class StdStringConstRef(StdStringBase):

  def __init__(self, kl_type_name, cpp_type_name):
    StdStringBase.__init__(self, kl_type_name, cpp_type_name)

  def gen_edk_ind_ret_param(self):
    return self.gen_edk_result_param()

  def gen_edk_store_result_pre(self):
    return self.gen_edk_result_name() + " = ";

  def gen_edk_store_result_post(self):
    return ".c_str()";

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return ""

  def gen_cpp_arg(self, edk_name, cpp_name):
    return self.gen_tmp_std_string(edk_name)

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return ""

class StdStringConstPtr(StdStringBase):

  def __init__(self, kl_type_name, cpp_type_name):
    StdStringBase.__init__(self, kl_type_name, cpp_type_name)

  def gen_edk_ind_ret_param(self):
    return self.gen_edk_result_param()

  def gen_edk_store_result_pre(self):
    return self.gen_edk_result_name() + " = ";

  def gen_edk_store_result_post(self):
    return ".c_str()";

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return self.gen_decl_std_string(edk_name, cpp_name)

  def gen_cpp_arg(self, edk_name, cpp_name):
    return self.gen_cpp_ptr_to(cpp_name)

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return ""

class StdStringMutableRef(StdStringBase):

  def __init__(self, kl_type_name, cpp_type_name):
    StdStringBase.__init__(self, kl_type_name, cpp_type_name)

  def gen_edk_ind_ret_param(self):
    return self.gen_edk_result_param()

  def gen_edk_store_result_pre(self):
    return self.gen_edk_result_name() + " = ";

  def gen_edk_store_result_post(self):
    return ".c_str()";

  def gen_kl_param(self, kl_name):
    return self.gen_kl_io_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_io_param(edk_name)

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return self.gen_decl_std_string(edk_name, cpp_name)

  def gen_cpp_arg(self, edk_name, cpp_name):
    return cpp_name

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return self.gen_upd_std_string(edk_name, cpp_name)

class StdStringMutablePtr(StdStringBase):

  def __init__(self, kl_type_name, cpp_type_name):
    StdStringBase.__init__(self, kl_type_name, cpp_type_name)

  def gen_kl_param(self, kl_name):
    return self.gen_kl_io_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_io_param(edk_name)

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return self.gen_decl_std_string(edk_name, cpp_name)

  def gen_cpp_arg(self, edk_name, cpp_name):
    return self.gen_cpp_ptr_to(cpp_name)

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return self.gen_upd_std_string(edk_name, cpp_name)
