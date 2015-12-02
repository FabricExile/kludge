from libkludge.type_codecs import *
from libkludge.ast import Param as ASTParam

# from edk_param import *

class TypeMgr:
  built_in_type_codecs = [
      SimpleValue("Boolean", "bool"),
      SimpleConstRef("Boolean", "const bool &"),
      SimpleConstPtr("Boolean", "const bool *"),
      SimpleMutableRef("Boolean", "bool &"),
      SimpleMutablePtr("Boolean", "bool *"),
      ###
      SimpleValue("SInt8", "signed char"),
      SimpleConstRef("SInt8", "const signed char &"),
      SimpleMutableRef("SInt8", "signed char &"),
      ###
      SimpleValue("UInt8", "unsigned char"),
      SimpleConstRef("UInt8", "const unsigned char &"),
      SimpleConstPtr("UInt8", "const unsigned char *"),
      SimpleMutableRef("UInt8", "unsigned char &"),
      SimpleMutablePtr("UInt8", "unsigned char *"),
      ###
      SimpleValue("SInt16", "short"),
      SimpleConstRef("SInt16", "const short &"),
      SimpleConstPtr("SInt16", "const short *"),
      SimpleMutableRef("SInt16", "short &"),
      SimpleMutablePtr("SInt16", "short *"),
      ###
      SimpleValue("UInt16", "unsigned short"),
      SimpleConstRef("UInt16", "const unsigned short &"),
      SimpleConstPtr("UInt16", "const unsigned short *"),
      SimpleMutableRef("UInt16", "unsigned short &"),
      SimpleMutablePtr("UInt16", "unsigned short *"),
      ###
      SimpleValue("SInt32", "int"),
      SimpleConstRef("SInt32", "const int &"),
      SimpleConstPtr("SInt32", "const int *"),
      SimpleMutableRef("SInt32", "int &"),
      SimpleMutablePtr("SInt32", "int *"),
      ###
      SimpleValue("UInt32", "unsigned int"),
      SimpleConstRef("UInt32", "const unsigned int &"),
      SimpleConstPtr("UInt32", "const unsigned int *"),
      SimpleMutableRef("UInt32", "unsigned int &"),
      SimpleMutablePtr("UInt32", "unsigned int *"),
      ###
      SimpleValue("SInt32", "long"),
      SimpleConstRef("SInt32", "const long &"),
      SimpleConstPtr("SInt32", "const long *"),
      SimpleMutableRef("SInt32", "long &"),
      SimpleMutablePtr("SInt32", "long *"),
      ###
      SimpleValue("UInt32", "unsigned long"),
      SimpleConstRef("UInt32", "const unsigned long &"),
      SimpleConstPtr("UInt32", "const unsigned long *"),
      SimpleMutableRef("UInt32", "unsigned long &"),
      SimpleMutablePtr("UInt32", "unsigned long *"),
      ###
      SimpleValue("SInt64", "long long"),
      SimpleConstRef("SInt64", "const long long &"),
      SimpleConstPtr("SInt64", "const long long *"),
      SimpleMutableRef("SInt64", "long long &"),
      SimpleMutablePtr("SInt64", "long long *"),
      ###
      SimpleValue("UInt64", "unsigned long long"),
      SimpleConstRef("UInt64", "const unsigned long long &"),
      SimpleConstPtr("UInt64", "const unsigned long long *"),
      SimpleMutableRef("UInt64", "unsigned long long &"),
      SimpleMutablePtr("UInt64", "unsigned long long *"),
      ###
      SimpleValue("Float32", "float"),
      SimpleConstRef("Float32", "const float &"),
      SimpleConstPtr("Float32", "const float *"),
      SimpleMutableRef("Float32", "float &"),
      SimpleMutablePtr("Float32", "float *"),
      ###
      SimpleValue("Float64", "double"),
      SimpleConstRef("Float64", "const double &"),
      SimpleConstPtr("Float64", "const double *"),
      SimpleMutableRef("Float64", "double &"),
      SimpleMutablePtr("Float64", "double *"),
      ###
      StdStringValue("String", "std::string"),
      StdStringConstRef("String", "const std::string &"),
      StdStringConstPtr("String", "const std::string *"),
      StdStringMutableRef("String", "std::string &"),
      StdStringMutablePtr("String", "std::string *"),
      ###
      CStringValue("String", "const char *"),
      CStringConstRef("String", "const char *const &"),
      ]

  def __init__(self):
    self._cpp_type_name_to_type_codec = {}

    self.add_type_codecs(TypeMgr.built_in_type_codecs)

  def add_type_codecs(self, type_codecs):
    for type_codec in type_codecs:
      self._cpp_type_name_to_type_codec[type_codec.cpp_type_name] = type_codec

  def get_type_codec(self, clang_type):
    cpp_type_name = clang_type.spelling
    if cpp_type_name == "void":
      return None

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
      lambda clang_param: ASTParam(
        clang_param.name,
        self.get_type_codec(clang_param.clang_type)
        ),
      clang_params
      )
