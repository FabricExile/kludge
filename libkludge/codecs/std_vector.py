from libkludge.codec import Codec
from libkludge.type_spec import TypeSpec, SimpleTypeSpec
from libkludge.gen_spec import GenStr, GenLambda
from libkludge.value_name import ValueName
from libkludge.cpp_type_expr_parser import *
from libkludge.cpp_type_expr_parser.helpers import *

def build_std_vector_codecs():

  def build_std_vector_type_spec(
    unqual_cpp_type_name,
    cpp_type_expr,
    element_type_info,
    ):
    return TypeSpec(
      element_type_info.kl.base,
      '[]' + element_type_info.kl.suffix,
      'VariableArray< ' + element_type_info.edk.name + ' >',
      unqual_cpp_type_name,
      cpp_type_expr,
      [element_type_info],
      )

  class StdVectorCodecBase(Codec): pass
  StdVectorCodecBase.conv(
    edk_to_cpp = """
{{ name.cpp }}.clear();
{{ name.cpp }}.reserve( {{ name.edk }}.size() );
for ( uint32_t i = 0; i < {{ name.edk }}.size(); ++i )
{
    {{ element.type.edk.name }} const &{{ element.name.edk }} = {{ name.edk }}[i];
    {{ element.conv_edk_to_cpp_decl() | indent(4) }}
    {{ name.cpp }}.push_back( {{ element.name.cpp }} );
}
""",
    edk_to_cpp_decl = GenLambda(
      lambda gd: gd.type.cpp.name + " " + gd.name.cpp + ";\n" + gd.conv_edk_to_cpp()
      ),
    cpp_to_edk = """
{{ name.edk }}.resize( 0 );
for ( {{ type.cpp.name }}::const_iterator it = {{ name.cpp }}.begin();
  it != {{ name.cpp }}.end(); ++it )
{
    {{ element.type.cpp.name }} const &{{ element.name.cpp }} = {{ element.traits_pointer_undo() }}*it;
    {{ element.conv_cpp_to_edk_decl() | indent(4) }}
    {{ name.edk }}.push( {{ element.name.edk }} );
}
""",
    cpp_to_edk_decl = GenLambda(
      lambda gd: gd.type.edk.name + " " + gd.name.edk + ";\n" + gd.conv_cpp_to_edk()
      ),
    )

  def element_if_std_vector(cpp_type_expr):
    if isinstance(cpp_type_expr, Template) \
      and cpp_type_expr.name == "std::vector" \
      and len(cpp_type_expr.params) == 1:
        return cpp_type_expr.params[0]

  def match_value(cls, cpp_type_expr, type_mgr):
    element_cpp_type_expr = element_if_std_vector(cpp_type_expr)
    if element_cpp_type_expr:
      element_type_info = type_mgr.maybe_get_type_info(element_cpp_type_expr)
      if element_type_info:
        return build_std_vector_type_spec(
          'std::vector< ' + element_type_info.cpp.qual_name + ' >',
          cpp_type_expr,
          element_type_info,
          )

  class StdVectorValueCodec(StdVectorCodecBase): pass
  StdVectorValueCodec.match(match_value)
  StdVectorValueCodec.traits_value()

  def match_const_ref(cls, cpp_type_expr, type_mgr):
    base_cpp_type_expr = pointee_if_const_ref(cpp_type_expr)
    if base_cpp_type_expr:
      element_cpp_type_expr = element_if_std_vector(base_cpp_type_expr)
      if element_cpp_type_expr:
        element_type_info = type_mgr.maybe_get_type_info(element_cpp_type_expr)
        if element_type_info:
          return build_std_vector_type_spec(
            'std::vector< ' + element_type_info.cpp.qual_name + ' >',
            cpp_type_expr,
            element_type_info,
            )

  class StdVectorConstRefCodec(StdVectorCodecBase): pass
  StdVectorConstRefCodec.match(match_const_ref)
  StdVectorConstRefCodec.traits_const_ref()

  return [
    StdVectorValueCodec,
    StdVectorConstRefCodec,
    ]
