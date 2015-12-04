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
        SimpleTypeSpec.builder('String')
      ).result_indirect(
        post = GenStr(".c_str()")
      ).in_param(
      ).no_conv(
        conv_arg_cpp = GenLambda(
          lambda gd: gd.name.edk + ".getCString()"
          ),
        conv_arg_edk = GenLambda(
          lambda gd: gd.name.cpp + ".c_str()"
          ),
      ),
    TypeCodec(
      jinjenv
      ).match_cpp_expr_type(
        PointerTo(Const(Named("std::string"))),
        SimpleTypeSpec.builder('String')
      ).result_indirect(
        post = GenStr(".c_str()")
      ).in_param(
      ).conv(
        conv_decl_cpp = GenLambda(
          lambda gd: "String " + gd.name.edk + ";"
          ),
        conv_edk_to_cpp = GenLambda(
          lambda gd: gd.name.cpp + " = std::string(" + gd.name.edk + ".getData(), " + gd.name.edk + ".getLength());"
          ),
        conv_arg_cpp = GenLambda(lambda gd: "&" + gd.name.cpp),
        conv_decl_edk = GenLambda(
          lambda gd: "std::string " + gd.name.cpp + ";"
          ),
        conv_cpp_to_edk = GenLambda(
          lambda gd: gd.name.edk + " = String(" + gd.name.cpp + ".size(), " + gd.name.cpp + ".data());"
          ),
        conv_arg_edk = GenLambda(lambda gd: gd.name.cpp),
      ),
    TypeCodec(
      jinjenv
      ).match_cpp_expr_type(
        ReferenceTo(Named("std::string")),
        SimpleTypeSpec.builder('String')
      ).result_indirect(
        post = GenStr(".c_str()")
      ).io_param(
      ).conv(
        conv_decl_cpp = GenLambda(
          lambda gd: "String " + gd.name.edk + ";"
          ),
        conv_edk_to_cpp = GenLambda(
          lambda gd: gd.name.cpp + " = std::string(" + gd.name.edk + ".getData(), " + gd.name.edk + ".getLength());"
          ),
        conv_arg_cpp = GenLambda(lambda gd: gd.name.cpp),
        conv_decl_edk = GenLambda(
          lambda gd: "std::string " + gd.name.cpp + ";"
          ),
        conv_cpp_to_edk = GenLambda(
          lambda gd: gd.name.edk + " = String(" + gd.name.cpp + ".size(), " + gd.name.cpp + ".data());"
          ),
        conv_arg_edk = GenLambda(lambda gd: gd.name.cpp),
      ),
    TypeCodec(
      jinjenv
      ).match_cpp_expr_type(
        PointerTo(Named("std::string")),
        SimpleTypeSpec.builder('String')
      ).no_result(
      ).io_param(
      ).conv(
        conv_edk_to_cpp = GenLambda(
          lambda gd: "std::string " + gd.name.cpp + "(" + gd.name.edk + ".getData(), " + gd.name.edk + ".getLength());"
          ),
        conv_arg_cpp = GenLambda(lambda gd: "&" + gd.name.cpp),
        conv_cpp_to_edk = GenLambda(
          lambda gd: gd.name.edk + " = String(" + gd.name.cpp + ".size(), " + gd.name.cpp + ".data());"
          ),
      ),
    ]
