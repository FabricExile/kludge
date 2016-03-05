from libkludge.codec import Codec
from libkludge.gen_spec import GenStr, GenLambda
from libkludge.type_spec import SimpleTypeSpec
from libkludge.cpp_type_expr_parser import *

def build_wrapped_ptr_codecs(class_name):
  class WrappedPtrCodecBase(Codec): pass
  WrappedPtrCodecBase.conv(
    edk_to_cpp = """
{{ name.cpp }} = *{{ name.edk }}.cpp_ptr;
""",
    edk_to_cpp_decl = GenLambda(
      lambda _: _.type.cpp.name + " " + _.name.cpp + ";\n" + _.conv_edk_to_cpp()
      ),
    cpp_to_edk = """
delete {{ name.edk }}.cpp_ptr;
{{ name.edk }}.cpp_ptr = new {{ type.cpp.name }}( {{ name.cpp }} );
""",
    cpp_to_edk_decl = """
{{ type.edk.name }} {{ name.edk }};
{{ name.edk }}.cpp_ptr = new {{ type.cpp.name }}( {{ name.cpp }} );
""",
    )
  WrappedPtrCodecBase.result(
    indirect_init_edk = """
{{ name.edk }}.cpp_ptr = 0;
""",
    )

  class WrappedPtrValueCodec(WrappedPtrCodecBase): pass
  WrappedPtrValueCodec.match_cpp_type_expr(
    Named(class_name),
    SimpleTypeSpec.builder(class_name, class_name)
    )
  WrappedPtrValueCodec.traits_value()

  class WrappedPtrConstRefCodec(WrappedPtrCodecBase): pass
  WrappedPtrConstRefCodec.match_cpp_type_expr(
    ReferenceTo(Const(Named(class_name))),
    SimpleTypeSpec.builder(class_name, class_name)
    )
  WrappedPtrConstRefCodec.traits_const_ref()

  return [
    WrappedPtrValueCodec,
    WrappedPtrConstRefCodec,
    ]
