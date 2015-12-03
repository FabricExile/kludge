from kludge import TypeCodec
from kludge.type_codecs.recipes import *
from kludge.CPPTypeExpr import *
from kludge import SimpleTypeName

def c_string_type_codec_generators(jinjenv, type_mgr):
  @match_cpp_expr_types(
    [
      PointerTo(Const(Char())),
      ReferenceTo(Const(PointerTo(Const(Char())))),
      ],
    SimpleTypeName('String', 'const char *')
    )
  @indirect_result()
  @in_param()
  @cpp_arg_is_edk_param(lambda cpp_arg: cpp_arg + ".getCString()")
  class CString(TypeCodec): pass

  return [CString]
