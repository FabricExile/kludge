import abc, clang

class EDKTypeMap:
  __metaclass__ = abc.ABCMeta

  def __init__(self, kl_type_name, cpp_type_name):
    self.kl_type_name = kl_type_name
    self.cpp_type_name = cpp_type_name

  @abc.abstractmethod
  def gen_dir_ret_type(self):
    """If KL type is direct return, the direct return type; else 'void'"""
    return

  @abc.abstractmethod
  def gen_ind_ref_param(self, name):
    """If KL type is indirect return, a parameter to hold the return value; else empty string"""
    return

  @abc.abstractmethod
  def gen_kl_param(self, kl_name):
    """Generate KL code for a parameter declaration"""
    return

  @abc.abstractmethod
  def gen_edk_param(self, edk_name):
    """A parameter of the given name"""
    return

  @abc.abstractmethod
  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    """Generate C++ code to convert an EDK parameter to a C++ argument"""
    return

  def gen_cpp_arg(self, edk_name, cpp_name):
    """Generate C++ code to pass a C++ argument to a C++ API call"""
    return

  @abc.abstractmethod
  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    """Generate C++ code to convert a C++ argument to an EDK parameter"""
    return

class SimpleValEDKTypeMap(EDKTypeMap):
  def __init__(self, kl_type_name, cpp_type_name):
    EDKTypeMap.__init__(self, kl_type_name, cpp_type_name)

  def gen_dir_ret_type(self, ):
    return "Traits<"+self.kl_type_name+">"

  def gen_ind_ref_param(self, edk_name):
    return ""

  def gen_kl_param(self, kl_name):
    return "in " + self.kl_type_name + " " + kl_name

  def gen_edk_param(self, edk_name):
    return "Traits<"+self.kl_type_name+">::INParam " + edk_name

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return ""

  def gen_cpp_arg(self, edk_name, cpp_name):
    return edk_name

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return ""

class CPPParam:
  def __init__(self, name, cpp_type_name):
    self.name = name
    self.cpp_type_name = cpp_type_name

class EDKParam:
  def __init__(self, name, edk_type_map):
    self.kl_name = name
    self.edk_name = name + "__EDK"
    self.cpp_name = name + "__CPP"
    self.edk_type_map = edk_type_map

  def gen_kl_param(self, is_last):
    result = self.edk_type_map.gen_kl_param(self.kl_name)
    if not is_last:
      result += ","
    return result

  def gen_edk_param(self, is_last):
    result = self.edk_type_map.gen_edk_param(self.edk_name)
    if not is_last:
      result += ","
    return result

  def gen_edk_param_to_cpp_arg(self):
    return self.edk_type_map.gen_edk_param_to_cpp_arg(self.edk_name, self.cpp_name)

  def gen_cpp_arg(self, is_last):
    result = self.edk_type_map.gen_cpp_arg(self.edk_name, self.cpp_name)
    if not is_last:
      result += ","
    return result

  def gen_cpp_arg_to_edk_param(self):
    return self.edk_type_map.gen_cpp_arg_to_edk_param(self.edk_name, self.cpp_name)

class EDKTypeMgr:
  def __init__(self):
    self.cpp_type_name_to_type_map = {}

    self.add_type_assoc(SimpleValEDKTypeMap("Boolean", "bool"))
    for cpp_type_name in ["int", "signed", "signed int"]:
      self.add_type_assoc(SimpleValEDKTypeMap("SInt32", cpp_type_name))
    for cpp_type_name in ["unsigned", "unsigned int"]:
      self.add_type_assoc(SimpleValEDKTypeMap("UInt32", cpp_type_name))

  def add_type_assoc(self, edk_type):
    self.cpp_type_name_to_type_map[edk_type.cpp_type_name] = edk_type

  def get_type(self, cpp_type_name):
    try:
      return self.cpp_type_name_to_type_map[cpp_type_name]
    except:
      raise Exception(cpp_type_name + ": no EDK type association found")

  def convert_cpp_params(self, cpp_params):
    return map(
      lambda cpp_param: EDKParam(
        cpp_param.name,
        self.get_type(cpp_param.cpp_type_name)
        ),
      cpp_params
      )
