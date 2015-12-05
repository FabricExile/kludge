from kludge import TypeCodec, GenLambda, SimpleTypeSpec
from kludge.CPPTypeExpr import *

def build_c_string_type_codecs():
  class CStringTypeCodecBase(TypeCodec): pass
  CStringTypeCodecBase.conv(
    edk_to_cpp = GenLambda(
      lambda gd: gd.name.cpp + " = " + gd.name.edk + ".getCString();"
      ),
    cpp_to_edk = GenLambda(
      lambda gd: gd.name.edk + " = " + gd.name.cpp + ";"
      ),
    )

  class CStringValueTypeCodec(CStringTypeCodecBase): pass
  CStringValueTypeCodec.match_cpp_type_expr(
    PointerTo(Const(Char())),
    SimpleTypeSpec.builder('String', 'char const *')
    )
  CStringValueTypeCodec.traits_value()

  class CStringConstRefTypeCodec(CStringTypeCodecBase): pass
  CStringConstRefTypeCodec.match_cpp_type_expr(
    ReferenceTo(Const(PointerTo(Const(Char())))),
    SimpleTypeSpec.builder('String', 'char const *')
    )
  CStringConstRefTypeCodec.traits_const_ref()

  return [
    CStringValueTypeCodec,
    CStringConstRefTypeCodec,
    ]
