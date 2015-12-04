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
        SimpleTypeSpec.builder('String')
      ).indirect_result(
      ).in_param(
      ).conv(
        cpp_arg = GenLambda(
          lambda gd: gd.name.edk + ".getCString()"
          )
      ),
    ]
