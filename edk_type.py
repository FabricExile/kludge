import clang

class EDKTypeMap:
  CPP_VARIANT_VAL = 0
  CPP_VARIANT_CONST_REF = 1
  CPP_VARIANT_CONST_PTR = 2
  CPP_VARIANT_MUTABLE_REF = 3
  CPP_VARIANT_MUTABLE_PTR = 4
  NUM_CPP_VARIANTS = 5

  CPP_VARIANT_BIT_VAL = 1 << CPP_VARIANT_VAL
  CPP_VARIANT_BIT_CONST_REF = 1 << CPP_VARIANT_CONST_REF
  CPP_VARIANT_BIT_CONST_PTR = 1 << CPP_VARIANT_CONST_PTR
  CPP_VARIANT_BIT_MUTABLE_REF = 1 << CPP_VARIANT_MUTABLE_REF
  CPP_VARIANT_BIT_MUTABLE_PTR = 1 << CPP_VARIANT_MUTABLE_PTR
  ALL_CPP_VARIANT_BITS = (1 << NUM_CPP_VARIANTS) - 1

  @staticmethod
  def raise_unsupported_as_ret(self, cpp_type_name):
    raise Exception(cpp_type_name + ": unsupported as return")

  @staticmethod
  def raise_unsupported_as_param(self, cpp_type_name):
    raise Exception(cpp_type_name + ": unsupported as parameter")

  def __init__(self, kl_type_name, cpp_base_type_name):
    self.kl_type_name = kl_type_name
    self.cpp_base_type_name = cpp_base_type_name

  cpp_type_name_gens = {
    CPP_VARIANT_VAL: lambda cpp_base_type_name: cpp_base_type_name,
    CPP_VARIANT_CONST_REF: lambda cpp_base_type_name: "const "+cpp_base_type_name+" &",
    CPP_VARIANT_CONST_PTR: lambda cpp_base_type_name: "const "+cpp_base_type_name+" *",
    CPP_VARIANT_MUTABLE_REF: lambda cpp_base_type_name: cpp_base_type_name+" &",
    CPP_VARIANT_MUTABLE_PTR: lambda cpp_base_type_name: cpp_base_type_name+" *",
  }

  def get_cpp_type_name(self, cpp_variant):
    return EDKTypeMap.cpp_type_name_gens[cpp_variant](self.cpp_base_type_name)

  def gen_dir_ret_type(self, cpp_variant):
    self.raise_unsupported_as_ret(self.get_cpp_type_name(cpp_variant))

  def gen_ind_ret_param(self, cpp_variant, name):
    self.raise_unsupported_as_ret(self.get_cpp_type_name(cpp_variant))

  def gen_kl_param(self, cpp_variant, kl_name):
    self.raise_unsupported_as_param(self.get_cpp_type_name(cpp_variant))

  def gen_edk_param(self, cpp_variant, edk_name):
    self.raise_unsupported_as_param(self.get_cpp_type_name(cpp_variant))

  def gen_edk_param_to_cpp_arg(self, cpp_variant, edk_name, cpp_name):
    self.raise_unsupported_as_param(self.get_cpp_type_name(cpp_variant))

  def gen_cpp_arg(self, cpp_variant, edk_name, cpp_name):
    self.raise_unsupported_as_param(self.get_cpp_type_name(cpp_variant))

  def gen_cpp_arg_to_edk_param(self, cpp_variant, edk_name, cpp_name):
    self.raise_unsupported_as_param(self.get_cpp_type_name(cpp_variant))

class EDKSimpleTypeMap(EDKTypeMap):
  def __init__(self, kl_type_name, cpp_base_type_name):
    EDKTypeMap.__init__(self, kl_type_name, cpp_base_type_name)

  dir_ret_type_gens = {
    EDKTypeMap.CPP_VARIANT_VAL:
      lambda cpp_type_name: cpp_type_name,
    EDKTypeMap.CPP_VARIANT_CONST_REF:
      lambda cpp_type_name: cpp_type_name,
    EDKTypeMap.CPP_VARIANT_CONST_PTR:
      lambda cpp_type_name: cpp_type_name,
    EDKTypeMap.CPP_VARIANT_MUTABLE_REF:
      lambda cpp_type_name: EDKTypeMap.raise_unsupported_as_ret(cpp_type_name),
    EDKTypeMap.CPP_VARIANT_MUTABLE_PTR:
      lambda cpp_type_name: EDKTypeMap.raise_unsupported_as_ret(cpp_type_name),
  }

  def gen_dir_ret_type(self, cpp_variant):
    return EDKSimpleTypeMap.dir_ret_type_gens[cpp_variant](self.get_cpp_type_name(cpp_variant))

  def gen_ind_ret_param(self, cpp_variant, edk_name):
    return ""

  kl_param_gens = {
    EDKTypeMap.CPP_VARIANT_VAL:
      lambda kl_type_name, kl_name: kl_type_name+" "+kl_name,
    EDKTypeMap.CPP_VARIANT_CONST_REF:
      lambda kl_type_name, kl_name: kl_type_name+" "+kl_name,
    EDKTypeMap.CPP_VARIANT_CONST_PTR:
      lambda kl_type_name, kl_name: kl_type_name+" "+kl_name,
    EDKTypeMap.CPP_VARIANT_MUTABLE_REF:
      lambda kl_type_name, kl_name: "io "+kl_type_name+" "+kl_name,
    EDKTypeMap.CPP_VARIANT_MUTABLE_PTR:
      lambda kl_type_name, kl_name: "io "+kl_type_name+" "+kl_name,
  }

  def gen_kl_param(self, cpp_variant, kl_name):
    return EDKSimpleTypeMap.kl_param_gens[cpp_variant](self.kl_type_name, kl_name)

  edk_param_gens = {
    EDKTypeMap.CPP_VARIANT_VAL:
      lambda kl_type_name, edk_name: "Traits<"+kl_type_name+">::INParam "+edk_name,
    EDKTypeMap.CPP_VARIANT_CONST_REF:
      lambda kl_type_name, edk_name: "Traits<"+kl_type_name+">::INParam "+edk_name,
    EDKTypeMap.CPP_VARIANT_CONST_PTR:
      lambda kl_type_name, edk_name: "Traits<"+kl_type_name+">::INParam "+edk_name,
    EDKTypeMap.CPP_VARIANT_MUTABLE_REF:
      lambda kl_type_name, edk_name: "Traits<"+kl_type_name+">::IOParam "+edk_name,
    EDKTypeMap.CPP_VARIANT_MUTABLE_PTR:
      lambda kl_type_name, edk_name: "Traits<"+kl_type_name+">::IOParam "+edk_name,
  }

  def gen_edk_param(self, cpp_variant, edk_name):
    return EDKSimpleTypeMap.edk_param_gens[cpp_variant](self.kl_type_name, edk_name)

  def gen_edk_param_to_cpp_arg(self, cpp_variant, edk_name, cpp_name):
    return ""

  cpp_arg_gens = {
    EDKTypeMap.CPP_VARIANT_VAL: lambda edk_name: edk_name,
    EDKTypeMap.CPP_VARIANT_CONST_REF: lambda edk_name: edk_name,
    EDKTypeMap.CPP_VARIANT_CONST_PTR: lambda edk_name: "&"+edk_name,
    EDKTypeMap.CPP_VARIANT_MUTABLE_REF: lambda edk_name: edk_name,
    EDKTypeMap.CPP_VARIANT_MUTABLE_PTR: lambda edk_name: "&"+edk_name,
  }

  def gen_cpp_arg(self, cpp_variant, edk_name, cpp_name):
    return EDKSimpleTypeMap.cpp_arg_gens[cpp_variant](edk_name)

  def gen_cpp_arg_to_edk_param(self, cpp_variant, edk_name, cpp_name):
    return ""

# class EDKStdStringTypeMap(EDKTypeMap):
#   def __init__(self):
#     EDKTypeMap.__init__(self, "String", "std::string")

#   def gen_dir_ret_type(self, cpp_variant):
#     return "void"

#   def gen_ind_ret_param(self, cpp_variant, edk_name):
#     return "Traits<String>::Result " + edk_name

#   def gen_kl_param(self, cpp_variant, kl_name):
#     return "String " + kl_name

#   def gen_edk_param(self, cpp_variant, edk_name):
#     return "Traits<String>::INParam " + edk_name

#   def gen_edk_param_to_cpp_arg(self, cpp_variant, edk_name, cpp_name):
#     return ""

#   def gen_cpp_arg(self, cpp_variant, edk_name, cpp_name):
#     return "std::string(" + edk_name + ".getData(), " + edk_name + ".getLength())"

#   def gen_cpp_arg_to_edk_param(self, cpp_variant, edk_name, cpp_name):
#     return ""

class EDKTypeCodec:
  def __init__(self, type_map, cpp_variant):
    self._type_map = type_map
    self._cpp_variant = cpp_variant

  @property
  def cpp_type_name(self):
    return self._type_map.get_cpp_type_name(self._cpp_variant)

  def gen_dir_ret_type(self):
    return self._type_map.gen_dir_ret_type(self._cpp_variant)

  def gen_ind_ret_param(self, name):
    return self._type_map.gen_ind_ret_param(self._cpp_variant, name)

  def gen_kl_param(self, kl_name):
    return self._type_map.gen_kl_param(self._cpp_variant, kl_name)

  def gen_edk_param(self, edk_name):
    return self._type_map.gen_edk_param(self._cpp_variant, edk_name)

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return self._type_map.gen_edk_param_to_cpp_arg(self._cpp_variant, edk_name, cpp_name)

  def gen_cpp_arg(self, edk_name, cpp_name):
    return self._type_map.gen_cpp_arg(self._cpp_variant, edk_name, cpp_name)

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return self._type_map.gen_cpp_arg_to_edk_param(self._cpp_variant, edk_name, cpp_name)

class ClangParam:
  def __init__(self, name, clang_type):
    self.name = name
    self.clang_type = clang_type

class EDKParam:
  def __init__(self, name, type_codec):
    self._kl_name = name
    self._edk_name = name + "__EDK"
    self._cpp_name = name + "__CPP"
    self._type_codec = type_codec

  def gen_kl_param(self, is_last):
    result = self._type_codec.gen_kl_param(self._kl_name)
    if not is_last:
      result += ","
    return result

  def gen_edk_param(self, is_last):
    result = self._type_codec.gen_edk_param(self._edk_name)
    if not is_last:
      result += ","
    return result

  def gen_edk_param_to_cpp_arg(self):
    return self._type_codec.gen_edk_param_to_cpp_arg(self._edk_name, self._cpp_name)

  def gen_cpp_arg(self, is_last):
    result = self._type_codec.gen_cpp_arg(self._edk_name, self._cpp_name)
    if not is_last:
      result += ","
    return result

  def gen_cpp_arg_to_edk_param(self):
    return self._type_codec.gen_cpp_arg_to_edk_param(self._edk_name, self._cpp_name)

class EDKTypeMgr:
  class SimpleType:
    def __init__(
      self,
      kl_type_name,
      cpp_base_type_names,
      cpp_variant_mask = EDKTypeMap.ALL_CPP_VARIANT_BITS
      ):
      self._kl_type_name = kl_type_name
      self._cpp_base_type_names = cpp_base_type_names
      self._cpp_variant_mask = cpp_variant_mask

    def add_type_codecs_to(self, type_mgr):
      for cpp_base_type_name in self._cpp_base_type_names:
        type_mgr.add_type_codecs(
          EDKSimpleTypeMap(self._kl_type_name, cpp_base_type_name),
          self._cpp_variant_mask
          )

  simple_types = [
    SimpleType("Boolean", ["bool"]),
    SimpleType(
      "SInt8", ["char", "signed char"],
      cpp_variant_mask=EDKTypeMap.CPP_VARIANT_BIT_VAL\
        |EDKTypeMap.CPP_VARIANT_BIT_MUTABLE_REF\
        |EDKTypeMap.CPP_VARIANT_BIT_CONST_REF
      ),
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
    self._cpp_type_name_to_type_codec = {}

    for simple_type in EDKTypeMgr.simple_types:
      simple_type.add_type_codecs_to(self)

    # self.add_type_codecs(EDKStdStringTypeMap())

  def add_type_codecs(self, type_map, cpp_variant_mask):
    for cpp_variant in range(0, EDKTypeMap.NUM_CPP_VARIANTS):
      if (1 << cpp_variant) & cpp_variant_mask:
        type_codec = EDKTypeCodec(type_map, cpp_variant)
        self._cpp_type_name_to_type_codec[type_codec.cpp_type_name] = type_codec

  def get_type_codec(self, clang_type):
    cpp_type_name = clang_type.spelling
    try:
      result = self._cpp_type_name_to_type_codec[cpp_type_name]
    except:
      try:
        canonical_cpp_type_name = clang_type.get_canonical().spelling
        result = self._cpp_type_name_to_type_codec[canonical_cpp_type_name]
        # update table for efficiency
        self._cpp_type_name_to_type_codec[cpp_type_name] = result
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
        self.get_type_codec(clang_param.clang_type)
        ),
      clang_params
      )
