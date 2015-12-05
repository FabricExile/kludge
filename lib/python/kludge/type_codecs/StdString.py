from kludge import TypeCodec, GenStr, GenLambda, SimpleTypeSpec
from kludge.CPPTypeExpr import *

def build_std_string_type_codecs():
  class StdStringTypeCodecBase(TypeCodec): pass
  StdStringTypeCodecBase.conv(
    edk_to_cpp = GenLambda(
      lambda gd: gd.name.cpp + " = " + gd.name.edk + ".getCString();"
      ),
    cpp_to_edk = GenLambda(
      lambda gd: gd.name.edk + " = " + gd.name.cpp + ".c_str();"
      ),
    )

  class StdStringValueTypeCodec(StdStringTypeCodecBase): pass
  StdStringValueTypeCodec.match_cpp_type_expr(
    Named("std::string"),
    SimpleTypeSpec.builder('String', 'std::string')
    )
  StdStringValueTypeCodec.traits_value()

  class StdStringConstRefTypeCodec(StdStringTypeCodecBase): pass
  StdStringConstRefTypeCodec.match_cpp_type_expr(
    ReferenceTo(Const(Named("std::string"))),
    SimpleTypeSpec.builder('String', 'std::string')
    )
  StdStringConstRefTypeCodec.traits_const_ref()

  class StdStringConstPtrTypeCodec(StdStringTypeCodecBase): pass
  StdStringConstPtrTypeCodec.match_cpp_type_expr(
    PointerTo(Const(Named("std::string"))),
    SimpleTypeSpec.builder('String', 'std::string')
    )
  StdStringConstPtrTypeCodec.traits_const_ptr()
  StdStringConstPtrTypeCodec.result_forbidden()

  class StdStringMutableRefTypeCodec(StdStringTypeCodecBase): pass
  StdStringMutableRefTypeCodec.match_cpp_type_expr(
    ReferenceTo(Named("std::string")),
    SimpleTypeSpec.builder('String', 'std::string')
    )
  StdStringMutableRefTypeCodec.traits_mutable_ref()
  StdStringMutableRefTypeCodec.param_io()

  class StdStringMutablePtrTypeCodec(StdStringTypeCodecBase): pass
  StdStringMutablePtrTypeCodec.match_cpp_type_expr(
    PointerTo(Named("std::string")),
    SimpleTypeSpec.builder('String', 'std::string')
    )
  StdStringMutablePtrTypeCodec.traits_mutable_ptr()
  StdStringMutablePtrTypeCodec.param_io()
  StdStringMutablePtrTypeCodec.result_forbidden()

  return [
    StdStringValueTypeCodec,
    StdStringConstRefTypeCodec,
    StdStringConstPtrTypeCodec,
    StdStringMutableRefTypeCodec,
    StdStringMutablePtrTypeCodec,
    ]
