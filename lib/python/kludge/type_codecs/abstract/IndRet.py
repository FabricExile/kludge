from kludge import TypeCodec

class IndRet(TypeCodec):

  def __init__(self, type_name):
    TypeCodec.__init__(self, type_name)

  def gen_direct_result_edk_type(self):
    return "void"

  def gen_edk_return_dir_result(self):
    return ""
