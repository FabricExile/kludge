import clang

class EDKTypeCodec:

  def __init__(
    self,
    kl_type_name,
    cpp_type_name,
    ):
    self.kl_type_name = kl_type_name
    self.cpp_type_name = cpp_type_name

  # Protocol: return

  def raise_unsupported_as_ret(self):
    raise self.cpp_type_name + ": unsupported as return"

  def gen_dir_ret_type(self):
    self.raise_unsupported_as_ret()

  def gen_ind_ret_param(self, edk_name):
    self.raise_unsupported_as_ret()

  # Protocol: parameters

  def raise_unsupported_as_param(self):
    raise self.cpp_type_name + ": unsupported as parameter"

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

  # Helpers

  def gen_kl_in_param(self, kl_name):
    return self.kl_type_name + " " + kl_name

  def gen_kl_io_param(self, kl_name):
    return "io " + self.kl_type_name + " " + kl_name

  def gen_edk_result(self, edk_name):
    return "Traits<" + self.kl_type_name + ">::Result " + edk_name

  def gen_edk_in_param(self, edk_name):
    return "Traits<" + self.kl_type_name + ">::INParam " + edk_name

  def gen_edk_io_param(self, edk_name):
    return "Traits<" + self.kl_type_name + ">::IOParam " + edk_name

  def gen_edk_ptr_to(self, edk_name):
    return "&" + edk_name

  def gen_cpp_ptr_to(self, cpp_name):
    return "&" + cpp_name

class EDKSimpleBaseTypeCodec(EDKTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKTypeCodec.__init__(self, kl_type_name, cpp_type_name)

  def gen_dir_ret_type(self):
    return self.cpp_type_name

  def gen_ind_ret_param(self, edk_name):
    return ""

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return ""

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return ""
  
class EDKSimpleValueTypeCodec(EDKSimpleBaseTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKSimpleBaseTypeCodec.__init__(self, kl_type_name, cpp_type_name)

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_cpp_arg(self, edk_name, cpp_name):
    return edk_name
  
class EDKSimpleConstRefTypeCodec(EDKSimpleBaseTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKSimpleBaseTypeCodec.__init__(self, kl_type_name, cpp_type_name)

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_cpp_arg(self, edk_name, cpp_name):
    return edk_name
  
class EDKSimpleConstPtrTypeCodec(EDKSimpleBaseTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKSimpleBaseTypeCodec.__init__(self, kl_type_name, cpp_type_name)

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_cpp_arg(self, edk_name, cpp_name):
    return self.gen_edk_ptr_to(edk_name)
  
class EDKSimpleMutableRefTypeCodec(EDKSimpleBaseTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKSimpleBaseTypeCodec.__init__(self, kl_type_name, cpp_type_name)

  def gen_kl_param(self, kl_name):
    return self.gen_kl_io_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_io_param(edk_name)

  def gen_cpp_arg(self, edk_name, cpp_name):
    return edk_name
  
class EDKSimpleMutablePtrTypeCodec(EDKSimpleBaseTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKSimpleBaseTypeCodec.__init__(self, kl_type_name, cpp_type_name)

  def gen_kl_param(self, kl_name):
    return self.gen_kl_io_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_io_param(edk_name)

  def gen_cpp_arg(self, edk_name, cpp_name):
    return self.gen_edk_ptr_to(edk_name)

class EDKIndRetTypeCodec(EDKTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKTypeCodec.__init__(self, kl_type_name, cpp_type_name)
  
  def gen_dir_ret_type(self):
    return "void"

  def gen_ind_ret_param(self, edk_name):
    return gen_edk_result(edk_name)

class EDKStdStringBaseTypeCodec(EDKIndRetTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKIndRetTypeCodec.__init__(self, kl_type_name, cpp_type_name)

  def gen_decl_std_string(self, edk_name, cpp_name):
    return "std::string " + cpp_name + "(" + edk_name + ".getData(), " + edk_name + ".getLength());"

  def gen_tmp_std_string(self, edk_name):
    return "std::string(" + edk_name + ".getData(), " + edk_name + ".getLength())"

  def gen_upd_std_string(self, edk_name, cpp_name):
    return edk_name + " = String(" + cpp_name + ".size(), " + cpp_name + ".data());"

class EDKStdStringValueTypeCodec(EDKStdStringBaseTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKStdStringBaseTypeCodec.__init__(self, kl_type_name, cpp_type_name)

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

class EDKStdStringConstRefTypeCodec(EDKStdStringBaseTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKStdStringBaseTypeCodec.__init__(self, kl_type_name, cpp_type_name)

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

class EDKStdStringConstPtrTypeCodec(EDKStdStringBaseTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKStdStringBaseTypeCodec.__init__(self, kl_type_name, cpp_type_name)

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

class EDKStdStringMutableRefTypeCodec(EDKStdStringBaseTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKStdStringBaseTypeCodec.__init__(self, kl_type_name, cpp_type_name)

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

class EDKStdStringMutablePtrTypeCodec(EDKStdStringBaseTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKStdStringBaseTypeCodec.__init__(self, kl_type_name, cpp_type_name)

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

class EDKCStringBaseTypeCodec(EDKIndRetTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKIndRetTypeCodec.__init__(self, kl_type_name, cpp_type_name)

  def gen_get_cstring(self, edk_name):
    return edk_name + ".getCString()"

class EDKCStringValueTypeCodec(EDKCStringBaseTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKCStringBaseTypeCodec.__init__(self, kl_type_name, cpp_type_name)

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return ""

  def gen_cpp_arg(self, edk_name, cpp_name):
    return self.gen_get_cstring(edk_name)

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return ""

class EDKCStringConstRefTypeCodec(EDKCStringBaseTypeCodec):

  def __init__(self, kl_type_name, cpp_type_name):
    EDKCStringBaseTypeCodec.__init__(self, kl_type_name, cpp_type_name)

  def gen_kl_param(self, kl_name):
    return self.gen_kl_in_param(kl_name)

  def gen_edk_param(self, edk_name):
    return self.gen_edk_in_param(edk_name)

  def gen_edk_param_to_cpp_arg(self, edk_name, cpp_name):
    return ""

  def gen_cpp_arg(self, edk_name, cpp_name):
    return self.gen_get_cstring(edk_name)

  def gen_cpp_arg_to_edk_param(self, edk_name, cpp_name):
    return ""

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
  built_in_type_codecs = [
      EDKSimpleValueTypeCodec("Boolean", "bool"),
      EDKSimpleConstRefTypeCodec("Boolean", "const bool &"),
      EDKSimpleConstPtrTypeCodec("Boolean", "const bool *"),
      EDKSimpleMutableRefTypeCodec("Boolean", "bool &"),
      EDKSimpleMutablePtrTypeCodec("Boolean", "bool *"),
      ###
      EDKSimpleValueTypeCodec("SInt8", "signed char"),
      EDKSimpleConstRefTypeCodec("SInt8", "const signed char &"),
      EDKSimpleMutableRefTypeCodec("SInt8", "signed char &"),
      ###
      EDKSimpleValueTypeCodec("UInt8", "unsigned char"),
      EDKSimpleConstRefTypeCodec("UInt8", "const unsigned char &"),
      EDKSimpleConstPtrTypeCodec("UInt8", "const unsigned char *"),
      EDKSimpleMutableRefTypeCodec("UInt8", "unsigned char &"),
      EDKSimpleMutablePtrTypeCodec("UInt8", "unsigned char *"),
      ###
      EDKSimpleValueTypeCodec("SInt16", "short"),
      EDKSimpleConstRefTypeCodec("SInt16", "const short &"),
      EDKSimpleConstPtrTypeCodec("SInt16", "const short *"),
      EDKSimpleMutableRefTypeCodec("SInt16", "short &"),
      EDKSimpleMutablePtrTypeCodec("SInt16", "short *"),
      ###
      EDKSimpleValueTypeCodec("UInt16", "unsigned short"),
      EDKSimpleConstRefTypeCodec("UInt16", "const unsigned short &"),
      EDKSimpleConstPtrTypeCodec("UInt16", "const unsigned short *"),
      EDKSimpleMutableRefTypeCodec("UInt16", "unsigned short &"),
      EDKSimpleMutablePtrTypeCodec("UInt16", "unsigned short *"),
      ###
      EDKSimpleValueTypeCodec("SInt32", "int"),
      EDKSimpleConstRefTypeCodec("SInt32", "const int &"),
      EDKSimpleConstPtrTypeCodec("SInt32", "const int *"),
      EDKSimpleMutableRefTypeCodec("SInt32", "int &"),
      EDKSimpleMutablePtrTypeCodec("SInt32", "int *"),
      ###
      EDKSimpleValueTypeCodec("UInt32", "unsigned int"),
      EDKSimpleConstRefTypeCodec("UInt32", "const unsigned int &"),
      EDKSimpleConstPtrTypeCodec("UInt32", "const unsigned int *"),
      EDKSimpleMutableRefTypeCodec("UInt32", "unsigned int &"),
      EDKSimpleMutablePtrTypeCodec("UInt32", "unsigned int *"),
      ###
      EDKSimpleValueTypeCodec("SInt64", "long long"),
      EDKSimpleConstRefTypeCodec("SInt64", "const long long &"),
      EDKSimpleConstPtrTypeCodec("SInt64", "const long long *"),
      EDKSimpleMutableRefTypeCodec("SInt64", "long long &"),
      EDKSimpleMutablePtrTypeCodec("SInt64", "long long *"),
      ###
      EDKSimpleValueTypeCodec("UInt64", "unsigned long long"),
      EDKSimpleConstRefTypeCodec("UInt64", "const unsigned long long &"),
      EDKSimpleConstPtrTypeCodec("UInt64", "const unsigned long long *"),
      EDKSimpleMutableRefTypeCodec("UInt64", "unsigned long long &"),
      EDKSimpleMutablePtrTypeCodec("UInt64", "unsigned long long *"),
      ###
      EDKSimpleValueTypeCodec("Float32", "float"),
      EDKSimpleConstRefTypeCodec("Float32", "const float &"),
      EDKSimpleConstPtrTypeCodec("Float32", "const float *"),
      EDKSimpleMutableRefTypeCodec("Float32", "float &"),
      EDKSimpleMutablePtrTypeCodec("Float32", "float *"),
      ###
      EDKSimpleValueTypeCodec("Float64", "double"),
      EDKSimpleConstRefTypeCodec("Float64", "const double &"),
      EDKSimpleConstPtrTypeCodec("Float64", "const double *"),
      EDKSimpleMutableRefTypeCodec("Float64", "double &"),
      EDKSimpleMutablePtrTypeCodec("Float64", "double *"),
      ###
      EDKStdStringValueTypeCodec("String", "std::string"),
      EDKStdStringConstRefTypeCodec("String", "const std::string &"),
      EDKStdStringConstPtrTypeCodec("String", "const std::string *"),
      EDKStdStringMutableRefTypeCodec("String", "std::string &"),
      EDKStdStringMutablePtrTypeCodec("String", "std::string *"),
      ###
      EDKCStringValueTypeCodec("String", "const char *"),
      EDKCStringConstRefTypeCodec("String", "const char *const &"),
      ]

  def __init__(self):
    self._cpp_type_name_to_type_codec = {}

    self.add_type_codecs(EDKTypeMgr.built_in_type_codecs)

  def add_type_codecs(self, type_codecs):
    for type_codec in type_codecs:
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
