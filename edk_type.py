import clang

class EDKTypeMap:
  def __init__(self, kl_type_name, cpp_type_name):
    self.kl_type_name = kl_type_name
    self.cpp_type_name = cpp_type_name

  def raise_unsupported_as_ret(self):
    raise Exception(self.cpp_type_name + ": unsupported as return")

  def gen_dir_ret_type(self):
    self.raise_unsupported_as_ret()

  def gen_ind_ret_param(self, name):
    self.raise_unsupported_as_ret()

  def raise_unsupported_as_param(self):
    raise Exception(self.cpp_type_name + ": unsupported as parameter")

  def gen_kl_param(self, kl_name):
    self.raise_unsupported_as_param()

  def gen_edk_param(self, edk_name):
    self.raise_unsupported_as_param()

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    self.raise_unsupported_as_param()

  def gen_cpp_arg(self, edk_name, cpp_name):
    self.raise_unsupported_as_param()

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    self.raise_unsupported_as_param()

def const_ref_cpp_type_name(cpp_type_name):
  return "const " + cpp_type_name + " &"

def mutable_ref_cpp_type_name(cpp_type_name):
  return cpp_type_name + " &"

def const_ptr_cpp_type_name(cpp_type_name):
  return "const " + cpp_type_name + " *"

def mutable_ptr_cpp_type_name(cpp_type_name):
  return cpp_type_name + " *"

class SimpleValEDKTypeMap(EDKTypeMap):
  def __init__(self, kl_type_name, cpp_type_name):
    EDKTypeMap.__init__(self, kl_type_name, cpp_type_name)

  def gen_dir_ret_type(self, ):
    return "Traits<"+self.kl_type_name+">"

  def gen_ind_ret_param(self, edk_name):
    return ""

  def gen_kl_param(self, kl_name):
    return self.kl_type_name + " " + kl_name

  def gen_edk_param(self, edk_name):
    return "Traits<"+self.kl_type_name+">::INParam " + edk_name

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return ""

  def gen_cpp_arg(self, edk_name, cpp_name):
    return edk_name

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return ""

class SimpleConstRefEDKTypeMap(EDKTypeMap):
  def __init__(self, kl_type_name, cpp_type_name):
    EDKTypeMap.__init__(self, kl_type_name, const_ref_cpp_type_name(cpp_type_name))

  def gen_dir_ret_type(self, ):
    return "Traits<"+self.kl_type_name+">"

  def gen_ind_ret_param(self, edk_name):
    return ""

  def gen_kl_param(self, kl_name):
    return self.kl_type_name + " " + kl_name

  def gen_edk_param(self, edk_name):
    return "Traits<"+self.kl_type_name+">::INParam " + edk_name

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return ""

  def gen_cpp_arg(self, edk_name, cpp_name):
    return edk_name

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return ""

class SimpleConstPtrEDKTypeMap(EDKTypeMap):
  def __init__(self, kl_type_name, cpp_type_name):
    EDKTypeMap.__init__(self, kl_type_name, const_ptr_cpp_type_name(cpp_type_name))

  def gen_kl_param(self, kl_name):
    return self.kl_type_name + " " + kl_name

  def gen_edk_param(self, edk_name):
    return "Traits<"+self.kl_type_name+">::INParam " + edk_name

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return ""

  def gen_cpp_arg(self, edk_name, cpp_name):
    return "&" + edk_name

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return ""

class SimpleMutableRefEDKTypeMap(EDKTypeMap):
  def __init__(self, kl_type_name, cpp_type_name):
    EDKTypeMap.__init__(self, kl_type_name, mutable_ref_cpp_type_name(cpp_type_name))

  def gen_kl_param(self, kl_name):
    return "io " + self.kl_type_name + " " + kl_name

  def gen_edk_param(self, edk_name):
    return "Traits<"+self.kl_type_name+">::IOParam " + edk_name

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return ""

  def gen_cpp_arg(self, edk_name, cpp_name):
    return edk_name

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return ""

class SimpleMutablePtrEDKTypeMap(EDKTypeMap):
  def __init__(self, kl_type_name, cpp_type_name):
    EDKTypeMap.__init__(self, kl_type_name, mutable_ptr_cpp_type_name(cpp_type_name))

  def gen_kl_param(self, kl_name):
    return "io " + self.kl_type_name + " " + kl_name

  def gen_edk_param(self, edk_name):
    return "Traits<"+self.kl_type_name+">::IOParam " + edk_name

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return ""

  def gen_cpp_arg(self, edk_name, cpp_name):
    return "&" + edk_name

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return ""

class StdStringValEDKTypeMap(EDKTypeMap):
  def __init__(self):
    EDKTypeMap.__init__(self, "String", "std::string")

  def gen_dir_ret_type(self, ):
    return "void"

  def gen_ind_ret_param(self, edk_name):
    return "Traits<String>::Result " + edk_name

  def gen_kl_param(self, kl_name):
    return "String " + kl_name

  def gen_edk_param(self, edk_name):
    return "Traits<String>::INParam " + edk_name

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return ""

  def gen_cpp_arg(self, edk_name, cpp_name):
    return "std::string(" + edk_name + ".getData(), " + edk_name + ".getLength())"

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return ""

class ClangParam:
  def __init__(self, name, clang_type):
    self.name = name
    self.clang_type = clang_type

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
  class SimpleType:
    def __init__(self, kl_type_name, cpp_type_names, allow_mutable_ptr=True):
      self._kl_type_name = kl_type_name
      self._cpp_type_names = cpp_type_names
      self._allow_mutable_ptr = allow_mutable_ptr

    def add_type_maps_to(self, type_mgr):
      for cpp_type_name in self._cpp_type_names:
        type_mgr.add_type_map(SimpleValEDKTypeMap(self._kl_type_name, cpp_type_name))
        type_mgr.add_type_map(SimpleConstRefEDKTypeMap(self._kl_type_name, cpp_type_name))
        type_mgr.add_type_map(SimpleMutableRefEDKTypeMap(self._kl_type_name, cpp_type_name))
        type_mgr.add_type_map(SimpleConstPtrEDKTypeMap(self._kl_type_name, cpp_type_name))
        if self._allow_mutable_ptr:
          type_mgr.add_type_map(SimpleMutablePtrEDKTypeMap(self._kl_type_name, cpp_type_name))

  simple_types = [
    SimpleType("Boolean", ["bool"]),
    SimpleType("SInt8", ["char", "signed char"], allow_mutable_ptr=False),
    SimpleType("UInt8", ["unsigned char"]),
    SimpleType("SInt16", ["short", "signed short"]),
    SimpleType("UInt16", ["unsigned short"]),
    SimpleType("SInt32", ["int", "signed int", "signed"]),
    SimpleType("UInt32", ["unsigned int", "unsigned"]),
    SimpleType("SInt64", ["long long", "signed long long"]),
    SimpleType("UInt64", ["unsigned long long"]),
    SimpleType("Float32", ["float"]),
    SimpleType("Float64", ["double"]),
    ]

  def __init__(self):
    self.cpp_type_name_to_type_map = {}

    for simple_type in EDKTypeMgr.simple_types:
      simple_type.add_type_maps_to(self)

    self.add_type_map(StdStringValEDKTypeMap())
    # self.add_type_map(StdStringConstRefEDKTypeMap())
    # self.add_type_map(StdStringConstPtrEDKTypeMap())
    # self.add_type_map(StdStringMutableRefEDKTypeMap())
    # self.add_type_map(StdStringMutablePtrEDKTypeMap())

  def add_type_map(self, edk_type):
    self.cpp_type_name_to_type_map[edk_type.cpp_type_name] = edk_type

  def get_type(self, clang_type):
    cpp_type_name = clang_type.spelling
    try:
      result = self.cpp_type_name_to_type_map[cpp_type_name]
    except:
      try:
        canonical_cpp_type_name = clang_type.get_canonical().spelling
        result = self.cpp_type_name_to_type_map[canonical_cpp_type_name]
        # update table for efficiency
        self.cpp_type_name_to_type_map[cpp_type_name] = result
      except:
        msg = cpp_type_name
        if canonical_cpp_type_name != cpp_type_name:
          msg += " ("
          msg += canonical_cpp_type_name
          msg += ")"
        msg += ": no EDK type association found"
        raise Exception(msg)
    return result

  def convert_clang_params(self, clang_params):
    return map(
      lambda clang_param: EDKParam(
        clang_param.name,
        self.get_type(clang_param.clang_type)
        ),
      clang_params
      )
