from kludge import TypeCodec, GenStr, GenLambda, SimpleTypeSpec
from kludge.CPPTypeExpr import *

def build_wrapped_ptr_type_codecs(class_name):
  class WrappedPtrTypeCodecBase(TypeCodec): pass
  WrappedPtrTypeCodecBase.conv(
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
  WrappedPtrTypeCodecBase.result(
    indirect_init_edk = """
{{ name.edk }}.cpp_ptr = 0;
""",
    )

  class WrappedPtrValueTypeCodec(WrappedPtrTypeCodecBase): pass
  WrappedPtrValueTypeCodec.match_cpp_type_expr(
    Named(class_name),
    SimpleTypeSpec.builder(class_name, class_name)
    )
  WrappedPtrValueTypeCodec.traits_value()

  class WrappedPtrConstRefTypeCodec(WrappedPtrTypeCodecBase): pass
  WrappedPtrConstRefTypeCodec.match_cpp_type_expr(
    ReferenceTo(Const(Named(class_name))),
    SimpleTypeSpec.builder(class_name, class_name)
    )
  WrappedPtrConstRefTypeCodec.traits_const_ref()

  return [
    WrappedPtrValueTypeCodec,
    WrappedPtrConstRefTypeCodec,
    ]
