from kludge import TypeCodec, GenStr, GenLambda, SimpleTypeSpec
from kludge.CPPTypeExpr import *

def build_std_string_type_codecs(jinjenv):
  return [
    TypeCodec(
      jinjenv
      ).match_cpp_expr_types([
          Named("std::string"),
          ReferenceTo(Const(Named("std::string"))),
        ],
        SimpleTypeSpec('String', 'std::string')
      ).conv(
        edk_to_cpp = GenLambda(
          lambda gd: gd.name.cpp + " = " + gd.name.edk + ".getCString();"
          ),
        cpp_to_edk = GenLambda(
          lambda gd: gd.name.edk + " = " + gd.name.cpp + ".c_str();"
          ),
      ).param_in(
      ).result_indirect(
      ),
    TypeCodec(
      jinjenv
      ).match_cpp_expr_type(
        PointerTo(Const(Named("std::string"))),
        SimpleTypeSpec('String', "std::string")
      ).conv(
        edk_to_cpp = GenLambda(
          lambda gd: gd.name.cpp + " = " + gd.name.edk + ".getCString();"
          ),
        cpp_to_edk = GenLambda(
          lambda gd: gd.name.edk + " = " + gd.name.cpp + ".c_str();"
          ),
      ).param_in_to_ptr(
      ).no_result(
      ),
    TypeCodec(
      jinjenv
      ).match_cpp_expr_type(
        ReferenceTo(Named("std::string")),
        SimpleTypeSpec('String', 'std::string')
      ).conv(
        edk_to_cpp = GenLambda(
          lambda gd: gd.name.cpp + " = " + gd.name.edk + ".getCString();"
          ),
        cpp_to_edk = GenLambda(
          lambda gd: gd.name.edk + " = " + gd.name.cpp + ".c_str();"
          ),
      ).param_io(
      ).result_indirect(
      ),
    TypeCodec(
      jinjenv
      ).match_cpp_expr_type(
        PointerTo(Named("std::string")),
        SimpleTypeSpec('String', 'std::string')
      ).conv(
        edk_to_cpp = GenLambda(
          lambda gd: gd.name.cpp + " = " + gd.name.edk + ".getCString();"
          ),
        cpp_to_edk = GenLambda(
          lambda gd: gd.name.edk + " = " + gd.name.cpp + ".c_str();"
          ),
      ).param_io_to_ptr(
      ).no_result(
      ),
    ]
