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
      ).indirect_result(
        post = GenStr(".c_str()")
      ).in_param(
      ).no_conv(
        cpp_arg = GenLambda(
          lambda gd: gd.name.edk + ".getCString()"
          )
      ),
    TypeCodec(
      jinjenv
      ).match_cpp_expr_type(
        PointerTo(Const(Named("std::string"))),
        SimpleTypeSpec.builder('String')
      ).indirect_result(
        post = GenStr(".c_str()")
      ).in_param(
      ).conv(
        edk_to_cpp = GenLambda(
          lambda gd: "std::string " + gd.name.cpp + "(" + gd.name.edk + ".getData(), " + gd.name.edk + ".getLength());"
          ),
        cpp_arg = GenLambda(lambda gd: "&" + gd.name.cpp),
        cpp_to_edk = GenStr(""),
      ),
    TypeCodec(
      jinjenv
      ).match_cpp_expr_type(
        ReferenceTo(Named("std::string")),
        SimpleTypeSpec.builder('String')
      ).indirect_result(
        post = GenStr(".c_str()")
      ).io_param(
      ).conv(
        edk_to_cpp = GenLambda(
          lambda gd: "std::string " + gd.name.cpp + "(" + gd.name.edk + ".getData(), " + gd.name.edk + ".getLength());"
          ),
        cpp_arg = GenLambda(lambda gd: gd.name.cpp),
        cpp_to_edk = GenLambda(
          lambda gd: gd.name.edk + " = String(" + gd.name.cpp + ".size(), " + gd.name.cpp + ".data());"
          ),
      ),
    TypeCodec(
      jinjenv
      ).match_cpp_expr_type(
        PointerTo(Named("std::string")),
        SimpleTypeSpec.builder('String')
      ).no_result(
      ).io_param(
      ).conv(
        edk_to_cpp = GenLambda(
          lambda gd: "std::string " + gd.name.cpp + "(" + gd.name.edk + ".getData(), " + gd.name.edk + ".getLength());"
          ),
        cpp_arg = GenLambda(lambda gd: "&" + gd.name.cpp),
        cpp_to_edk = GenLambda(
          lambda gd: gd.name.edk + " = String(" + gd.name.cpp + ".size(), " + gd.name.cpp + ".data());"
          ),
      ),
    ]
