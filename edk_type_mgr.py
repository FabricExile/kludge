from edk_simple_type_codec import *
from edk_std_string_type_codec import *
from edk_c_string_type_codec import *

from edk_param import *

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
      EDKSimpleValueTypeCodec("SInt32", "long"),
      EDKSimpleConstRefTypeCodec("SInt32", "const long &"),
      EDKSimpleConstPtrTypeCodec("SInt32", "const long *"),
      EDKSimpleMutableRefTypeCodec("SInt32", "long &"),
      EDKSimpleMutablePtrTypeCodec("SInt32", "long *"),
      ###
      EDKSimpleValueTypeCodec("UInt32", "unsigned long"),
      EDKSimpleConstRefTypeCodec("UInt32", "const unsigned long &"),
      EDKSimpleConstPtrTypeCodec("UInt32", "const unsigned long *"),
      EDKSimpleMutableRefTypeCodec("UInt32", "unsigned long &"),
      EDKSimpleMutablePtrTypeCodec("UInt32", "unsigned long *"),
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
