from kludge import TypeName, SimpleTypeName
from kludge.type_codecs import *
from kludge.ast import Param as ASTParam
from kludge import CPPTypeExpr

# from edk_param import *

class TypeMgr:

  built_in_type_codec_generators = [
    CString, # First so we don't catch in Simple...
    SimpleValue,
    SimpleConstRef,
    SimpleConstPtr,
    SimpleMutableRef,
    SimpleMutablePtr,
    StdVectorValue,
    StdVectorConstRef,
    StdStringValue,
    StdStringConstRef,
    StdStringConstPtr,
    StdStringMutableRef,
    StdStringMutablePtr,
    ]

  def __init__(self):
    self._cpp_type_name_to_type_codec = {}
    self._type_codec_generators = []
    self._cpp_type_expr_parser = CPPTypeExpr.Parser()

    self.add_type_codec_generators(self.built_in_type_codec_generators)

  def add_type_codec_generator(self, type_codec_generator):
    self._type_codec_generators.append(type_codec_generator)

  def add_type_codec_generators(self, type_codec_generators):
    for type_codec_generator in type_codec_generators:
      self.add_type_codec_generator(type_codec_generator)

  def add_type_codec(self, type_codec):
    self._cpp_type_name_to_type_codec[type_codec.type_name.cpp] = type_codec

  def add_type_codecs(self, type_codecs):
    for type_codec in type_codecs:
      self.add_type_codec(type_codec)

  def maybe_get_type_codec(self, cpp_type_name):
    if cpp_type_name == "void":
      return None

    result = self._cpp_type_name_to_type_codec.get(cpp_type_name)
    if not result:
      try:
        cpp_type_expr = self._cpp_type_expr_parser.parse(cpp_type_name)
      except:
        raise Exception(cpp_type_name + ": malformed C++ type expression")

      for type_codec_generator in self._type_codec_generators:
        type_codec = type_codec_generator.maybe_get_type_codec(cpp_type_expr, self)
        if type_codec:
          self.add_type_codec(type_codec)
          result = type_codec
          break
    return result

  def get_type_codec(self, cpp_type_name):
    if cpp_type_name == "void":
      return None

    type_codec = self.maybe_get_type_codec(cpp_type_name)
    if type_codec:
      return type_codec

    raise Exception(cpp_type_name + ": no EDK type association found")

  def get_type_codec_for_clang_type(self, clang_type):
    return self.get_type_codec(clang_type.spelling)

  def convert_clang_params(self, clang_params):
    return map(
      lambda clang_param: ASTParam(
        clang_param.name,
        self.get_type_codec_for_clang_type(clang_param.clang_type)
        ),
      clang_params
      )
