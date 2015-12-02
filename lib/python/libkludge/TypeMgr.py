from libkludge import TypeName, SimpleTypeName
from libkludge.type_codecs import *
from libkludge.ast import Param as ASTParam

# from edk_param import *

class TypeMgr:
  built_in_type_codecs = [
      SimpleValue(SimpleTypeName("Boolean", "bool")),
      SimpleConstRef(SimpleTypeName("Boolean", "const bool &")),
      SimpleConstPtr(SimpleTypeName("Boolean", "const bool *")),
      SimpleMutableRef(SimpleTypeName("Boolean", "bool &")),
      SimpleMutablePtr(SimpleTypeName("Boolean", "bool *")),
      ###
      SimpleValue(SimpleTypeName("SInt8", "signed char")),
      SimpleConstRef(SimpleTypeName("SInt8", "const signed char &")),
      SimpleMutableRef(SimpleTypeName("SInt8", "signed char &")),
      ###
      SimpleValue(SimpleTypeName("UInt8", "unsigned char")),
      SimpleConstRef(SimpleTypeName("UInt8", "const unsigned char &")),
      SimpleConstPtr(SimpleTypeName("UInt8", "const unsigned char *")),
      SimpleMutableRef(SimpleTypeName("UInt8", "unsigned char &")),
      SimpleMutablePtr(SimpleTypeName("UInt8", "unsigned char *")),
      ###
      SimpleValue(SimpleTypeName("SInt16", "short")),
      SimpleConstRef(SimpleTypeName("SInt16", "const short &")),
      SimpleConstPtr(SimpleTypeName("SInt16", "const short *")),
      SimpleMutableRef(SimpleTypeName("SInt16", "short &")),
      SimpleMutablePtr(SimpleTypeName("SInt16", "short *")),
      ###
      SimpleValue(SimpleTypeName("UInt16", "unsigned short")),
      SimpleConstRef(SimpleTypeName("UInt16", "const unsigned short &")),
      SimpleConstPtr(SimpleTypeName("UInt16", "const unsigned short *")),
      SimpleMutableRef(SimpleTypeName("UInt16", "unsigned short &")),
      SimpleMutablePtr(SimpleTypeName("UInt16", "unsigned short *")),
      ###
      SimpleValue(SimpleTypeName("SInt32", "int")),
      SimpleConstRef(SimpleTypeName("SInt32", "const int &")),
      SimpleConstPtr(SimpleTypeName("SInt32", "const int *")),
      SimpleMutableRef(SimpleTypeName("SInt32", "int &")),
      SimpleMutablePtr(SimpleTypeName("SInt32", "int *")),
      ###
      SimpleValue(SimpleTypeName("UInt32", "unsigned int")),
      SimpleConstRef(SimpleTypeName("UInt32", "const unsigned int &")),
      SimpleConstPtr(SimpleTypeName("UInt32", "const unsigned int *")),
      SimpleMutableRef(SimpleTypeName("UInt32", "unsigned int &")),
      SimpleMutablePtr(SimpleTypeName("UInt32", "unsigned int *")),
      ###
      SimpleValue(SimpleTypeName("SInt32", "long")),
      SimpleConstRef(SimpleTypeName("SInt32", "const long &")),
      SimpleConstPtr(SimpleTypeName("SInt32", "const long *")),
      SimpleMutableRef(SimpleTypeName("SInt32", "long &")),
      SimpleMutablePtr(SimpleTypeName("SInt32", "long *")),
      ###
      SimpleValue(SimpleTypeName("UInt32", "unsigned long")),
      SimpleConstRef(SimpleTypeName("UInt32", "const unsigned long &")),
      SimpleConstPtr(SimpleTypeName("UInt32", "const unsigned long *")),
      SimpleMutableRef(SimpleTypeName("UInt32", "unsigned long &")),
      SimpleMutablePtr(SimpleTypeName("UInt32", "unsigned long *")),
      ###
      SimpleValue(SimpleTypeName("SInt64", "long long")),
      SimpleConstRef(SimpleTypeName("SInt64", "const long long &")),
      SimpleConstPtr(SimpleTypeName("SInt64", "const long long *")),
      SimpleMutableRef(SimpleTypeName("SInt64", "long long &")),
      SimpleMutablePtr(SimpleTypeName("SInt64", "long long *")),
      ###
      SimpleValue(SimpleTypeName("UInt64", "unsigned long long")),
      SimpleConstRef(SimpleTypeName("UInt64", "const unsigned long long &")),
      SimpleConstPtr(SimpleTypeName("UInt64", "const unsigned long long *")),
      SimpleMutableRef(SimpleTypeName("UInt64", "unsigned long long &")),
      SimpleMutablePtr(SimpleTypeName("UInt64", "unsigned long long *")),
      ###
      SimpleValue(SimpleTypeName("Float32", "float")),
      SimpleConstRef(SimpleTypeName("Float32", "const float &")),
      SimpleConstPtr(SimpleTypeName("Float32", "const float *")),
      SimpleMutableRef(SimpleTypeName("Float32", "float &")),
      SimpleMutablePtr(SimpleTypeName("Float32", "float *")),
      ###
      SimpleValue(SimpleTypeName("Float64", "double")),
      SimpleConstRef(SimpleTypeName("Float64", "const double &")),
      SimpleConstPtr(SimpleTypeName("Float64", "const double *")),
      SimpleMutableRef(SimpleTypeName("Float64", "double &")),
      SimpleMutablePtr(SimpleTypeName("Float64", "double *")),
      ###
      StdStringValue(SimpleTypeName("String", "std::string")),
      StdStringConstRef(SimpleTypeName("String", "const std::string &")),
      StdStringConstPtr(SimpleTypeName("String", "const std::string *")),
      StdStringMutableRef(SimpleTypeName("String", "std::string &")),
      StdStringMutablePtr(SimpleTypeName("String", "std::string *")),
      ###
      CStringValue(SimpleTypeName("String", "const char *")),
      CStringConstRef(SimpleTypeName("String", "const char *const &")),
      ]

  def __init__(self):
    self._cpp_type_name_to_type_codec = {}

    self.add_type_codecs(TypeMgr.built_in_type_codecs)

    self.add_type_codecs([
      StdVectorValue(TypeName("Float32", "[]", "VariableArray<Float32>", "std::vector<float>"), SimpleValue(SimpleTypeName("Float32", "float"))),
      StdVectorValue(TypeName("Float32", "[]", "VariableArray<Float32>", "const std::vector<float> &"), SimpleValue(SimpleTypeName("Float32", "float"))),
      ])

  def add_type_codecs(self, type_codecs):
    for type_codec in type_codecs:
      self._cpp_type_name_to_type_codec[type_codec.type_name.cpp] = type_codec

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
