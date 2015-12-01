import clang

class CPPTypeModIndex:
  Value = 0
  ConstRef = 1
  ConstPtr = 2
  MutableRef = 3
  MutablePtr = 4

  COUNT = 5

class CPPTypeModBits:
  Value = 1 << CPPTypeModIndex.Value
  ConstRef = 1 << CPPTypeModIndex.ConstRef
  ConstPtr = 1 << CPPTypeModIndex.ConstPtr
  MutableRef = 1 << CPPTypeModIndex.MutableRef
  MutablePtr = 1 << CPPTypeModIndex.MutablePtr

  ALL = (1 << CPPTypeModIndex.COUNT) - 1

class CPPTypeVar:
  def __init__(self, base_name, mod_index):
    self.base_name = base_name
    self.mod_index = mod_index

  cpp_type_name_gens = {
    CPPTypeModIndex.Value: lambda cpp_base_type_name: cpp_base_type_name,
    CPPTypeModIndex.ConstRef: lambda cpp_base_type_name: "const "+cpp_base_type_name+" &",
    CPPTypeModIndex.ConstPtr: lambda cpp_base_type_name: "const "+cpp_base_type_name+" *",
    CPPTypeModIndex.MutableRef: lambda cpp_base_type_name: cpp_base_type_name+" &",
    CPPTypeModIndex.MutablePtr: lambda cpp_base_type_name: cpp_base_type_name+" *",
  }

  @property
  def name(self):
    return CPPTypeVar.cpp_type_name_gens[self.mod_index](self.base_name)

class EDKTypeCodec:
  @staticmethod
  def raise_unsupported_as_ret(self, cpp_type_name):
    raise Exception(cpp_type_name + ": unsupported as return")

  @staticmethod
  def raise_unsupported_as_param(self, cpp_type_name):
    raise Exception(cpp_type_name + ": unsupported as parameter")

  def __init__(self, kl_type_name):
    self.kl_type_name = kl_type_name

  def gen_dir_ret_type(self, cpp_type_var):
    self.raise_unsupported_as_ret(cpp_type_var.name)

  def gen_ind_ret_param(self, cpp_type_var, name):
    self.raise_unsupported_as_ret(cpp_type_var.name)

  def gen_kl_param(self, cpp_type_var, kl_name):
    self.raise_unsupported_as_param(cpp_type_var.name)

  def gen_edk_param(self, cpp_type_var, edk_name):
    self.raise_unsupported_as_param(cpp_type_var.name)

  def gen_edk_param_to_cpp_arg(self, cpp_type_var, edk_name, cpp_name):
    self.raise_unsupported_as_param(cpp_type_var.name)

  def gen_cpp_arg(self, cpp_type_var, edk_name, cpp_name):
    self.raise_unsupported_as_param(cpp_type_var.name)

  def gen_cpp_arg_to_edk_param(self, cpp_type_var, edk_name, cpp_name):
    self.raise_unsupported_as_param(cpp_type_var.name)

class EDKSimpleTypeMap(EDKTypeCodec):
  def __init__(self, kl_type_name):
    EDKTypeCodec.__init__(self, kl_type_name)

  dir_ret_type_gens = {
    CPPTypeModIndex.Value:
      lambda cpp_type_name: cpp_type_name,
    CPPTypeModIndex.ConstRef:
      lambda cpp_type_name: cpp_type_name,
    CPPTypeModIndex.ConstPtr:
      lambda cpp_type_name: cpp_type_name,
    CPPTypeModIndex.MutableRef:
      lambda cpp_type_name: EDKTypeCodec.raise_unsupported_as_ret(cpp_type_name),
    CPPTypeModIndex.MutablePtr:
      lambda cpp_type_name: EDKTypeCodec.raise_unsupported_as_ret(cpp_type_name),
  }

  def gen_dir_ret_type(self, cpp_type_var):
    return EDKSimpleTypeMap.dir_ret_type_gens[cpp_type_var.mod_index](cpp_type_var.name)

  def gen_ind_ret_param(self, cpp_type_var, edk_name):
    return ""

  kl_param_gens = {
    CPPTypeModIndex.Value:
      lambda kl_type_name, kl_name: kl_type_name+" "+kl_name,
    CPPTypeModIndex.ConstRef:
      lambda kl_type_name, kl_name: kl_type_name+" "+kl_name,
    CPPTypeModIndex.ConstPtr:
      lambda kl_type_name, kl_name: kl_type_name+" "+kl_name,
    CPPTypeModIndex.MutableRef:
      lambda kl_type_name, kl_name: "io "+kl_type_name+" "+kl_name,
    CPPTypeModIndex.MutablePtr:
      lambda kl_type_name, kl_name: "io "+kl_type_name+" "+kl_name,
  }

  def gen_kl_param(self, cpp_type_var, kl_name):
    return EDKSimpleTypeMap.kl_param_gens[cpp_type_var.mod_index](self.kl_type_name, kl_name)

  edk_param_gens = {
    CPPTypeModIndex.Value:
      lambda kl_type_name, edk_name: "Traits<"+kl_type_name+">::INParam "+edk_name,
    CPPTypeModIndex.ConstRef:
      lambda kl_type_name, edk_name: "Traits<"+kl_type_name+">::INParam "+edk_name,
    CPPTypeModIndex.ConstPtr:
      lambda kl_type_name, edk_name: "Traits<"+kl_type_name+">::INParam "+edk_name,
    CPPTypeModIndex.MutableRef:
      lambda kl_type_name, edk_name: "Traits<"+kl_type_name+">::IOParam "+edk_name,
    CPPTypeModIndex.MutablePtr:
      lambda kl_type_name, edk_name: "Traits<"+kl_type_name+">::IOParam "+edk_name,
  }

  def gen_edk_param(self, cpp_type_var, edk_name):
    return EDKSimpleTypeMap.edk_param_gens[cpp_type_var.mod_index](self.kl_type_name, edk_name)

  def gen_edk_param_to_cpp_arg(self, cpp_type_var, edk_name, cpp_name):
    return ""

  cpp_arg_gens = {
    CPPTypeModIndex.Value: lambda edk_name: edk_name,
    CPPTypeModIndex.ConstRef: lambda edk_name: edk_name,
    CPPTypeModIndex.ConstPtr: lambda edk_name: "&"+edk_name,
    CPPTypeModIndex.MutableRef: lambda edk_name: edk_name,
    CPPTypeModIndex.MutablePtr: lambda edk_name: "&"+edk_name,
  }

  def gen_cpp_arg(self, cpp_type_var, edk_name, cpp_name):
    return EDKSimpleTypeMap.cpp_arg_gens[cpp_type_var.mod_index](edk_name)

  def gen_cpp_arg_to_edk_param(self, cpp_type_var, edk_name, cpp_name):
    return ""

# class EDKStdStringTypeMap(EDKTypeCodec):
#   def __init__(self):
#     EDKTypeCodec.__init__(self, "String", "std::string")

#   def gen_dir_ret_type(self, cpp_type_mod):
#     return "void"

#   def gen_ind_ret_param(self, cpp_type_mod, edk_name):
#     return "Traits<String>::Result " + edk_name

#   def gen_kl_param(self, cpp_type_mod, kl_name):
#     return "String " + kl_name

#   def gen_edk_param(self, cpp_type_mod, edk_name):
#     return "Traits<String>::INParam " + edk_name

#   def gen_edk_param_to_cpp_arg(self, cpp_type_mod, edk_name, cpp_name):
#     return ""

#   def gen_cpp_arg(self, cpp_type_mod, edk_name, cpp_name):
#     return "std::string(" + edk_name + ".getData(), " + edk_name + ".getLength())"

#   def gen_cpp_arg_to_edk_param(self, cpp_type_mod, edk_name, cpp_name):
#     return ""

class EDKTypeMap:
  def __init__(self, type_codec, cpp_type_var):
    self._type_codec = type_codec
    self._cpp_type_var = cpp_type_var

  @property
  def cpp_type_name(self):
    return self._type_codec.get_cpp_type_name(self._cpp_type_var)

  def gen_dir_ret_type(self):
    return self._type_codec.gen_dir_ret_type(self._cpp_type_var)

  def gen_ind_ret_param(self, name):
    return self._type_codec.gen_ind_ret_param(self._cpp_type_var, name)

  def gen_kl_param(self, kl_name):
    return self._type_codec.gen_kl_param(self._cpp_type_var, kl_name)

  def gen_edk_param(self, edk_name):
    return self._type_codec.gen_edk_param(self._cpp_type_var, edk_name)

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return self._type_codec.gen_edk_param_to_cpp_arg(self._cpp_type_var, edk_name, cpp_name)

  def gen_cpp_arg(self, edk_name, cpp_name):
    return self._type_codec.gen_cpp_arg(self._cpp_type_var, edk_name, cpp_name)

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return self._type_codec.gen_cpp_arg_to_edk_param(self._cpp_type_var, edk_name, cpp_name)

class ClangParam:
  def __init__(self, name, clang_type):
    self.name = name
    self.clang_type = clang_type

class EDKParam:
  def __init__(self, name, type_map):
    self._kl_name = name
    self._edk_name = name + "__EDK"
    self._cpp_name = name + "__CPP"
    self._type_map = type_map

  def gen_kl_param(self, is_last):
    result = self._type_map.gen_kl_param(self._kl_name)
    if not is_last:
      result += ","
    return result

  def gen_edk_param(self, is_last):
    result = self._type_map.gen_edk_param(self._edk_name)
    if not is_last:
      result += ","
    return result

  def gen_edk_param_to_cpp_arg(self):
    return self._type_map.gen_edk_param_to_cpp_arg(self._edk_name, self._cpp_name)

  def gen_cpp_arg(self, is_last):
    result = self._type_map.gen_cpp_arg(self._edk_name, self._cpp_name)
    if not is_last:
      result += ","
    return result

  def gen_cpp_arg_to_edk_param(self):
    return self._type_map.gen_cpp_arg_to_edk_param(self._edk_name, self._cpp_name)

class EDKTypeMgr:
  def __init__(self):
    self._cpp_type_name_to_type_map = {}

    self.add_type_maps(
      EDKSimpleTypeMap("Boolean"),
      ["bool"],
      ),
    self.add_type_maps(
      EDKSimpleTypeMap("SInt8"),
      ["char", "signed char"],
      cpp_type_mod_mask=CPPTypeModBits.Value|CPPTypeModBits.MutableRef|CPPTypeModBits.ConstRef
      ),
    self.add_type_maps(
      EDKSimpleTypeMap("UInt8"),
      ["unsigned char"],
      ),
    self.add_type_maps(
      EDKSimpleTypeMap("SInt16"),
      ["short", "signed short"],
      ),
    self.add_type_maps(
      EDKSimpleTypeMap("UInt16"),
      ["unsigned short"],
      ),
    self.add_type_maps(
      EDKSimpleTypeMap("SInt32"),
      ["int", "signed int", "signed"],
      ),
    self.add_type_maps(
      EDKSimpleTypeMap("UInt32"),
      ["unsigned int", "unsigned"],
      ),
    self.add_type_maps(
      EDKSimpleTypeMap("SInt64"),
      ["long long", "signed long long"],
      ),
    self.add_type_maps(
      EDKSimpleTypeMap("UInt64"),
      ["unsigned long long"],
      ),
    self.add_type_maps(
      EDKSimpleTypeMap("Float32"),
      ["float"],
      ),
    self.add_type_maps(
      EDKSimpleTypeMap("Float64"),
      ["double"],
      ),

    # self.add_type_maps(EDKStdStringTypeMap())

  def add_type_maps(
    self,
    type_codec,
    cpp_base_type_names,
    cpp_type_mod_mask = CPPTypeModBits.ALL
    ):
    for cpp_base_type_name in cpp_base_type_names:
      for cpp_type_mod_index in range(0, CPPTypeModIndex.COUNT):
        if (1 << cpp_type_mod_index) & cpp_type_mod_mask:
          type_var = CPPTypeVar(cpp_base_type_name, cpp_type_mod_index)
          self._cpp_type_name_to_type_map[type_var.name] = EDKTypeMap(type_codec, type_var)

  def get_type_map(self, clang_type):
    cpp_type_name = clang_type.spelling
    try:
      result = self._cpp_type_name_to_type_map[cpp_type_name]
    except:
      try:
        canonical_cpp_type_name = clang_type.get_canonical().spelling
        result = self._cpp_type_name_to_type_map[canonical_cpp_type_name]
        # update table for efficiency
        self._cpp_type_name_to_type_map[cpp_type_name] = result
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
        self.get_type_map(clang_param.clang_type)
        ),
      clang_params
      )
