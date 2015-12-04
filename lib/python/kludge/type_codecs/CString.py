from kludge import TypeCodec
from kludge.CPPTypeExpr import *
from kludge import SimpleTypeSpec

def c_string_type_codecs(jinjenv):
  type_codec = TypeCodec(jinjenv)
  type_codec.match_cpp_expr_types(
    [
      PointerTo(Const(Char())),
      ReferenceTo(Const(PointerTo(Const(Char())))),
      ],
    SimpleTypeSpec.builder('String')
    )
  type_codec.indirect_result()
  type_codec.in_param()
  type_codec.conv(
    cpp_arg = "{{ name.edk }}.getCString()"
    )

  return [type_codec]
