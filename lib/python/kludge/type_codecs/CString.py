from kludge import TypeCodec, GenLambda, SimpleTypeSpec
from kludge.CPPTypeExpr import *

def build_c_string_type_codecs(jinjenv):
  return [
    TypeCodec(
      jinjenv
      ).match_cpp_type_expr(
        PointerTo(Const(Char())),
        SimpleTypeSpec.builder('String', 'char const *')
      ).traits_value(
      ).conv(
        edk_to_cpp = GenLambda(
          lambda gd: gd.name.cpp + " = " + gd.name.edk + ".getCString();"
          ),
        cpp_to_edk = GenLambda(
          lambda gd: gd.name.edk + " = " + gd.name.cpp + ";"
          ),
      ),
    TypeCodec(
      jinjenv
      ).match_cpp_type_expr(
        ReferenceTo(Const(PointerTo(Const(Char())))),
        SimpleTypeSpec.builder('String', 'char const *')
      ).traits_const_ref(
      ).conv(
        edk_to_cpp = GenLambda(
          lambda gd: gd.name.cpp + " = " + gd.name.edk + ".getCString();"
          ),
        cpp_to_edk = GenLambda(
          lambda gd: gd.name.edk + " = " + gd.name.cpp + ";"
          ),
      ),
    ]
