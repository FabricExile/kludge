from kludge.type_codecs.abstract import IndRet
from kludge import CPPTypeExpr
from kludge import SimpleTypeName

class AllocatedCopiedWrapperBase(IndRet):

  def __init__(self, type_name):
    IndRet.__init__(self, type_name)

class AllocatedCopiedWrapperValue(AllocatedCopiedWrapperBase):

  def __init__(self, type_name):
    AllocatedCopiedWrapperBase.__init__(self, type_name)

  def gen_edk_ind_ret_param(self):
    return self.gen_edk_result_param()

  def gen_edk_store_result_pre(self):
    edk_name = self.gen_edk_result_name()
    return "%s.cpp_ptr = new %s(" % (edk_name, self.type_name.cpp)

  def gen_edk_store_result_post(self):
    return ")";

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return ""

  def gen_cpp_arg(self, edk_name, cpp_name):
    return "*" + edk_name + ".cpp_ptr"

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return ""

class AllocatedCopiedWrapperConstRef(AllocatedCopiedWrapperValue):

  def __init__(self, type_name):
    AllocatedCopiedWrapperValue.__init__(self, type_name)
