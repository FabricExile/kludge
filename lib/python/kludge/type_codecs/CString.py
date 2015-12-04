from kludge import TypeCodec, GenLambda, SimpleTypeSpec
from kludge.CPPTypeExpr import *

def build_c_string_type_codecs(jinjenv):
  return [
    TypeCodec(
      jinjenv
      ).match_cpp_expr_types(
        [
          PointerTo(Const(Char())),
          ReferenceTo(Const(PointerTo(Const(Char())))),
          ],
        SimpleTypeSpec('String', 'char const *')
      ).conv(
        edk_to_cpp = GenLambda(
          lambda gd: gd.name.cpp + " = " + gd.name.edk + ".getCString();"
          ),
        cpp_to_edk = GenLambda(
          lambda gd: gd.name.edk + " = " + gd.name.cpp + ";"
          ),
      ).result_indirect(
      ).param_in(
      ),
    ]
