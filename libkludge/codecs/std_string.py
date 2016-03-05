from libkludge.codec import Codec
from libkludge.gen_spec import GenStr, GenLambda
from libkludge.type_spec import SimpleTypeSpec
from libkludge.cpp_type_expr_parser import *

def build_std_string_type_codecs():
  class StdStringCodecBase(Codec): pass
  StdStringCodecBase.conv(
    edk_to_cpp = GenLambda(
      lambda gd: gd.name.cpp + " = " + gd.name.edk + ".getCString();"
      ),
    cpp_to_edk = GenLambda(
      lambda gd: gd.name.edk + " = " + gd.name.cpp + ".c_str();"
      ),
    )

  class StdStringValueCodec(StdStringCodecBase): pass
  StdStringValueCodec.match_cpp_type_expr(
    Named("std::string"),
    SimpleTypeSpec.builder('String', 'std::string')
    )
  StdStringValueCodec.traits_value()

  class StdStringConstRefCodec(StdStringCodecBase): pass
  StdStringConstRefCodec.match_cpp_type_expr(
    ReferenceTo(Const(Named("std::string"))),
    SimpleTypeSpec.builder('String', 'std::string')
    )
  StdStringConstRefCodec.traits_const_ref()

  class StdStringConstPtrCodec(StdStringCodecBase): pass
  StdStringConstPtrCodec.match_cpp_type_expr(
    PointerTo(Const(Named("std::string"))),
    SimpleTypeSpec.builder('String', 'std::string')
    )
  StdStringConstPtrCodec.traits_const_ptr()
  StdStringConstPtrCodec.result_forbidden()

  class StdStringMutableRefCodec(StdStringCodecBase): pass
  StdStringMutableRefCodec.match_cpp_type_expr(
    ReferenceTo(Named("std::string")),
    SimpleTypeSpec.builder('String', 'std::string')
    )
  StdStringMutableRefCodec.traits_mutable_ref()
  StdStringMutableRefCodec.param_io()

  class StdStringMutablePtrCodec(StdStringCodecBase): pass
  StdStringMutablePtrCodec.match_cpp_type_expr(
    PointerTo(Named("std::string")),
    SimpleTypeSpec.builder('String', 'std::string')
    )
  StdStringMutablePtrCodec.traits_mutable_ptr()
  StdStringMutablePtrCodec.param_io()
  StdStringMutablePtrCodec.result_forbidden()

  return [
    StdStringValueCodec,
    StdStringConstRefCodec,
    StdStringConstPtrCodec,
    StdStringMutableRefCodec,
    StdStringMutablePtrCodec,
    ]
