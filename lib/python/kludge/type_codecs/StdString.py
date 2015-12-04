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
        SimpleTypeSpec.builder('String', 'std::string')
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
        SimpleTypeSpec.builder('String')
      ).conv(
        edk_to_cpp = GenLambda(
          lambda gd: gd.name.cpp + " = " + gd.name.edk + ".getCString();"
          ),
        cpp_to_edk = GenLambda(
          lambda gd: gd.name.edk + " = " + gd.name.cpp + ".c_str();"
          ),
      ).param_in(
        cpp = GenLambda(
          lambda gd: "&" + gd.name.cpp
          )
      
      ).result_indirect(
        decl_and_assign_cpp = GenLambda(
          lambda gd: gd.conv_decl_cpp() + "\n  " + gd.name.cpp + " = *"
        )
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
