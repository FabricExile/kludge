import clang, re

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
  cpp_type_name_gens = {
    CPPTypeModIndex.Value:
      lambda cpp_base_type_name: cpp_base_type_name,
    CPPTypeModIndex.ConstRef:
      lambda cpp_base_type_name:
        cpp_base_type_name+"const &" \
          if cpp_base_type_name.endswith(("*", "&")) \
          else "const "+cpp_base_type_name+" &",
    CPPTypeModIndex.ConstPtr:
      lambda cpp_base_type_name:
        cpp_base_type_name+"const *" \
          if cpp_base_type_name.endswith(("*", "&")) \
          else "const "+cpp_base_type_name+" *",
    CPPTypeModIndex.MutableRef:
      lambda cpp_base_type_name: cpp_base_type_name+" &",
    CPPTypeModIndex.MutablePtr:
      lambda cpp_base_type_name: cpp_base_type_name+" *",
  }

  def __init__(self, base_name, mod_index):
    self.base_name = base_name
    self.mod_index = mod_index
    self.name = CPPTypeVar.cpp_type_name_gens[mod_index](base_name)

class EDKTypeCodec:
  def __init__(self, kl_type_name):
    self.kl_type_name = kl_type_name

  def gen_dir_ret_type(self, cpp_type_var):
    return "void"

  ind_ret_param_gens = {
    CPPTypeModIndex.Value:
      lambda edk_name: "Traits<String>::Result "+edk_name,
    CPPTypeModIndex.ConstRef:
      lambda edk_name: "Traits<String>::Result "+edk_name,
    CPPTypeModIndex.ConstPtr:
      lambda edk_name: "Traits<String>::Result "+edk_name,
  }

  def gen_ind_ret_param(self, cpp_type_var, edk_name):
    return EDKStdStringTypeCodec.ind_ret_param_gens[cpp_type_var.mod_index](edk_name)

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
    return EDKSimpleTypeCodec.kl_param_gens[cpp_type_var.mod_index](self.kl_type_name, kl_name)

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
    return EDKSimpleTypeCodec.edk_param_gens[cpp_type_var.mod_index](self.kl_type_name, edk_name)

  def gen_edk_param_to_cpp_arg(self, cpp_type_var, edk_name, cpp_name):
    return ""

  def gen_cpp_arg_to_edk_param(self, cpp_type_var, edk_name, cpp_name):
    return ""

class EDKSimpleTypeCodec(EDKTypeCodec):
  def __init__(self, kl_type_name):
    EDKTypeCodec.__init__(self, kl_type_name)

  dir_ret_type_gens = {
    CPPTypeModIndex.Value:
      lambda cpp_type_name: cpp_type_name,
    CPPTypeModIndex.ConstRef:
      lambda cpp_type_name: cpp_type_name,
    CPPTypeModIndex.ConstPtr:
      lambda cpp_type_name: cpp_type_name,
  }

  def gen_dir_ret_type(self, cpp_type_var):
    return EDKSimpleTypeCodec.dir_ret_type_gens[cpp_type_var.mod_index](cpp_type_var.name)

  def gen_ind_ret_param(self, cpp_type_var, edk_name):
    return ""

  cpp_arg_gens = {
    CPPTypeModIndex.Value: lambda edk_name: edk_name,
    CPPTypeModIndex.ConstRef: lambda edk_name: edk_name,
    CPPTypeModIndex.ConstPtr: lambda edk_name: "&"+edk_name,
    CPPTypeModIndex.MutableRef: lambda edk_name: edk_name,
    CPPTypeModIndex.MutablePtr: lambda edk_name: "&"+edk_name,
  }

  def gen_cpp_arg(self, cpp_type_var, edk_name, cpp_name):
    return EDKSimpleTypeCodec.cpp_arg_gens[cpp_type_var.mod_index](edk_name)

class EDKStdStringTypeCodec(EDKTypeCodec):
  def __init__(self):
    EDKTypeCodec.__init__(self, "String")

  edk_param_to_cpp_arg_gens = {
    CPPTypeModIndex.Value:
      lambda edk_name, cpp_name: "",
    CPPTypeModIndex.ConstRef:
      lambda edk_name, cpp_name: "",
    CPPTypeModIndex.ConstPtr:
      lambda edk_name, cpp_name:
        "std::string "+cpp_name+"("+edk_name+".getData(), "+edk_name+".getLength());",
    CPPTypeModIndex.MutableRef:
      lambda edk_name, cpp_name:
        "std::string "+cpp_name+"("+edk_name+".getData(), "+edk_name+".getLength());",
    CPPTypeModIndex.MutablePtr:
      lambda edk_name, cpp_name:
        "std::string "+cpp_name+"("+edk_name+".getData(), "+edk_name+".getLength());",
  }

  def gen_edk_param_to_cpp_arg(self, cpp_type_var, edk_name, cpp_name):
    return EDKStdStringTypeCodec.edk_param_to_cpp_arg_gens[cpp_type_var.mod_index](edk_name, cpp_name)

  cpp_arg_gens = {
    CPPTypeModIndex.Value:
      lambda edk_name, cpp_name:
        "std::string("+edk_name+".getData(), "+edk_name+".getLength())",
    CPPTypeModIndex.ConstRef:
      lambda edk_name, cpp_name:
        "std::string("+edk_name+".getData(), "+edk_name+".getLength())",
    CPPTypeModIndex.ConstPtr:
      lambda edk_name, cpp_name: "&"+cpp_name,
    CPPTypeModIndex.MutableRef:
      lambda edk_name, cpp_name: cpp_name,
    CPPTypeModIndex.MutablePtr:
      lambda edk_name, cpp_name: "&"+cpp_name,
  }

  def gen_cpp_arg(self, cpp_type_var, edk_name, cpp_name):
    return EDKStdStringTypeCodec.cpp_arg_gens[cpp_type_var.mod_index](edk_name, cpp_name)

  cpp_arg_to_edk_param_gens = {
    CPPTypeModIndex.Value:
      lambda edk_name, cpp_name: "",
    CPPTypeModIndex.ConstRef:
      lambda edk_name, cpp_name: "",
    CPPTypeModIndex.ConstPtr:
      lambda edk_name, cpp_name: "",
    CPPTypeModIndex.MutableRef:
      lambda edk_name, cpp_name:
        edk_name+" = String("+cpp_name+".size(), "+cpp_name+".data());",
    CPPTypeModIndex.MutablePtr:
      lambda edk_name, cpp_name:
        edk_name+" = String("+cpp_name+".size(), "+cpp_name+".data());",
  }

  def gen_cpp_arg_to_edk_param(self, cpp_type_var, edk_name, cpp_name):
    return EDKStdStringTypeCodec.cpp_arg_to_edk_param_gens[cpp_type_var.mod_index](edk_name, cpp_name)

class EDKCStringTypeCodec(EDKTypeCodec):
  def __init__(self):
    EDKTypeCodec.__init__(self, "String")

  cpp_arg_gens = {
    CPPTypeModIndex.Value:
      lambda edk_name, cpp_name:
        edk_name+".getCString()",
  }

  def gen_cpp_arg(self, cpp_type_var, edk_name, cpp_name):
    return EDKCStringTypeCodec.cpp_arg_gens[cpp_type_var.mod_index](edk_name, cpp_name)

class EDKTypeMap:
  def __init__(self, type_codec, type_var):
    self._type_codec = type_codec
    self._type_var = type_var

  def raise_unsupported_as_ret(self):
    raise Exception(self._type_var.name + ": unsupported as return")

  def gen_dir_ret_type(self):
    try:
      return self._type_codec.gen_dir_ret_type(self._type_var)
    except:
      self.raise_unsupported_as_ret()

  def gen_ind_ret_param(self, name):
    try:
      return self._type_codec.gen_ind_ret_param(self._type_var, name)
    except:
      self.raise_unsupported_as_ret()

  def raise_unsupported_as_param(self):
    raise Exception(self._type_var.name + ": unsupported as parameter")

  def gen_kl_param(self, kl_name):
    try:
      return self._type_codec.gen_kl_param(self._type_var, kl_name)
    except:
      self.raise_unsupported_as_param()

  def gen_edk_param(self, edk_name):
    try:
      return self._type_codec.gen_edk_param(self._type_var, edk_name)
    except:
      self.raise_unsupported_as_param()

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    try:
      return self._type_codec.gen_edk_param_to_cpp_arg(self._type_var, edk_name, cpp_name)
    except:
      self.raise_unsupported_as_param()

  def gen_cpp_arg(self, edk_name, cpp_name):
    try:
      return self._type_codec.gen_cpp_arg(self._type_var, edk_name, cpp_name)
    except:
      self.raise_unsupported_as_param()

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    try:
      return self._type_codec.gen_cpp_arg_to_edk_param(self._type_var, edk_name, cpp_name)
    except:
      self.raise_unsupported_as_param()

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
      EDKSimpleTypeCodec("Boolean"),
      ["bool"],
      )
    self.add_type_maps(
      EDKSimpleTypeCodec("SInt8"),
      ["char", "signed char"],
      cpp_type_mod_mask=CPPTypeModBits.Value|CPPTypeModBits.MutableRef|CPPTypeModBits.ConstRef
      )
    self.add_type_maps(
      EDKSimpleTypeCodec("UInt8"),
      ["unsigned char"],
      )
    self.add_type_maps(
      EDKSimpleTypeCodec("SInt16"),
      ["short", "signed short"],
      )
    self.add_type_maps(
      EDKSimpleTypeCodec("UInt16"),
      ["unsigned short"],
      )
    self.add_type_maps(
      EDKSimpleTypeCodec("SInt32"),
      ["int", "signed int", "signed"],
      )
    self.add_type_maps(
      EDKSimpleTypeCodec("UInt32"),
      ["unsigned int", "unsigned"],
      )
    self.add_type_maps(
      EDKSimpleTypeCodec("SInt64"),
      ["long long", "signed long long"],
      )
    self.add_type_maps(
      EDKSimpleTypeCodec("UInt64"),
      ["unsigned long long"],
      )
    self.add_type_maps(
      EDKSimpleTypeCodec("Float32"),
      ["float"],
      )
    self.add_type_maps(
      EDKSimpleTypeCodec("Float64"),
      ["double"],
      )

    self.add_type_maps(
      EDKCStringTypeCodec(),
      ["const char *"],
      cpp_type_mod_mask=CPPTypeModBits.Value|CPPTypeModBits.ConstRef
      )

    self.add_type_maps(
      EDKStdStringTypeCodec(),
      ["std::string"],
      )

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
          print "Adding " + type_var.name
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
