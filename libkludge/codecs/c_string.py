from libkludge.codec import Codec
from libkludge.gen_spec import GenLambda
from libkludge.type_spec import SimpleTypeSpec
from libkludge.cpp_type_expr_parser import *

def build_c_string_codecs():
  class CStringCodecBase(Codec): pass
  CStringCodecBase.conv(
    edk_to_cpp = GenLambda(
      lambda gd: gd.name.cpp + " = " + gd.name.edk + ".getCString();"
      ),
    cpp_to_edk = GenLambda(
      lambda gd: gd.name.edk + " = " + gd.name.cpp + ";"
      ),
    )

  class CStringValueCodec(CStringCodecBase): pass
  CStringValueCodec.match_cpp_type_expr(
    PointerTo(Const(Char())),
    SimpleTypeSpec.builder('String', 'char const *')
    )
  CStringValueCodec.traits_value()

  class CStringConstRefCodec(CStringCodecBase): pass
  CStringConstRefCodec.match_cpp_type_expr(
    ReferenceTo(Const(PointerTo(Const(Char())))),
    SimpleTypeSpec.builder('String', 'char const *')
    )
  CStringConstRefCodec.traits_const_ref()

  return [
    CStringValueCodec,
    CStringConstRefCodec,
    ]
