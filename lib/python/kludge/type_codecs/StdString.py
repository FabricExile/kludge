from kludge import TypeCodec, GenStr, GenLambda, SimpleTypeSpec
from kludge.CPPTypeExpr import *

def build_std_string_type_codecs():
  return [
    TypeCodec(
      ).match_cpp_type_expr(
        Named("std::string"),
        SimpleTypeSpec.builder('String', 'std::string')
      ).traits_value(
      ).conv(
        edk_to_cpp = GenLambda(
          lambda gd: gd.name.cpp + " = " + gd.name.edk + ".getCString();"
          ),
        cpp_to_edk = GenLambda(
          lambda gd: gd.name.edk + " = " + gd.name.cpp + ".c_str();"
          ),
      ),
    TypeCodec(
      ).match_cpp_type_expr(
        ReferenceTo(Const(Named("std::string"))),
        SimpleTypeSpec.builder('String', 'std::string')
      ).traits_const_ref(
      ).conv(
        edk_to_cpp = GenLambda(
          lambda gd: gd.name.cpp + " = " + gd.name.edk + ".getCString();"
          ),
        cpp_to_edk = GenLambda(
          lambda gd: gd.name.edk + " = " + gd.name.cpp + ".c_str();"
          ),
      ),
    TypeCodec(
      ).match_cpp_type_expr(
        PointerTo(Const(Named("std::string"))),
        SimpleTypeSpec.builder('String', "std::string")
      ).traits_const_ptr(
      ).conv(
        edk_to_cpp = GenLambda(
          lambda gd: gd.name.cpp + " = " + gd.name.edk + ".getCString();"
          ),
        cpp_to_edk = GenLambda(
          lambda gd: gd.name.edk + " = " + gd.name.cpp + ".c_str();"
          ),
      ).result_forbidden(
      ),
    TypeCodec(
      ).match_cpp_type_expr(
        ReferenceTo(Named("std::string")),
        SimpleTypeSpec.builder('String', 'std::string')
      ).traits_mutable_ref(
      ).conv(
        edk_to_cpp = GenLambda(
          lambda gd: gd.name.cpp + " = " + gd.name.edk + ".getCString();"
          ),
        cpp_to_edk = GenLambda(
          lambda gd: gd.name.edk + " = " + gd.name.cpp + ".c_str();"
          ),
      ).param_io(
      ),
    TypeCodec(
      ).match_cpp_type_expr(
        PointerTo(Named("std::string")),
        SimpleTypeSpec.builder('String', 'std::string')
      ).traits_mutable_ptr(
      ).conv(
        edk_to_cpp = GenLambda(
          lambda gd: gd.name.cpp + " = " + gd.name.edk + ".getCString();"
          ),
        cpp_to_edk = GenLambda(
          lambda gd: gd.name.edk + " = " + gd.name.cpp + ".c_str();"
          ),
      ).param_io(
      ).result_forbidden(
      ),
    ]
