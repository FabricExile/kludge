from kludge import TypeSpec, TypeCodec, GenStr, GenLambda, SimpleTypeSpec, ValueName, Value
from kludge.CPPTypeExpr import *
from kludge.CPPTypeExpr.helpers import *

def build_std_vector_type_codecs():

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

  class StdVectorTypeCodecBase(TypeCodec): pass
  StdVectorTypeCodecBase.conv(
    edk_to_cpp = """
    {{ name.cpp }}.clear();
    {{ name.cpp }}.reserve( {{ name.edk }}.size() );
    for ( uint32_t i = 0; i < {{ name.edk }}.size(); ++i )
    {
        {{ element.type.edk.name }} const &{{ element.name.edk }} = {{ name.edk }}[i];
        {{ element.conv_edk_to_cpp_decl() }}
        {{ name.cpp }}.push_back( {{ element.name.cpp }} );
    }
""",
    edk_to_cpp_decl = GenLambda(
      lambda gd: gd.type.cpp.name + " " + gd.name.cpp + ";\n    " + gd.conv_edk_to_cpp()
      ),
    cpp_to_edk = """
    {{ name.edk }}.resize( 0 );
    for ( {{ type.cpp.name }}::const_iterator it = {{ name.cpp }}.begin();
      it != {{ name.cpp }}.end(); ++it )
    {
        {{ element.type.cpp.name }} const &{{ element.name.cpp }} = {{ element.traits_pointer_undo() }}*it;
        {{ element.conv_cpp_to_edk_decl() }}
        {{ name.edk }}.push( {{ element.name.edk }} );
    }
""",
    cpp_to_edk_decl = GenLambda(
      lambda gd: gd.type.edk.name + " " + gd.name.edk + ";\n    " + gd.conv_cpp_to_edk()
      ),
    )

  def is_std_vector(cpp_type_expr):
    return isinstance(cpp_type_expr, Template) \
      and cpp_type_expr.name == "std::vector"

  def match_value(cls, cpp_type_expr, type_mgr):
    if is_std_vector(cpp_type_expr):
      element_cpp_type_expr = cpp_type_expr.params[0]
      element_type_info = type_mgr.maybe_get_type_info(element_cpp_type_expr)
      if element_type_info:
        return build_std_vector_type_spec(
          'std::vector< ' + element_type_info.cpp.qual_name + ' >',
          cpp_type_expr,
          element_type_info,
          )

  class StdVectorValueTypeCodec(StdVectorTypeCodecBase): pass
  StdVectorValueTypeCodec.match(match_value)
  StdVectorValueTypeCodec.traits_value()

  def match_const_ref(cls, cpp_type_expr, type_mgr):
    if is_const_ref(cpp_type_expr):
      base_cpp_type_expr = cpp_type_expr.pointee
      if is_std_vector(base_cpp_type_expr):
        element_cpp_type_expr = base_cpp_type_expr.params[0]
        element_type_info = type_mgr.maybe_get_type_info(element_cpp_type_expr)
        if element_type_info:
          return build_std_vector_type_spec(
            'std::vector< ' + element_type_info.cpp.qual_name + ' >',
            cpp_type_expr,
            element_type_info,
            )

  class StdVectorConstRefTypeCodec(StdVectorTypeCodecBase): pass
  StdVectorConstRefTypeCodec.match(match_const_ref)
  StdVectorConstRefTypeCodec.traits_const_ref()

  return [
    StdVectorValueTypeCodec,
    StdVectorConstRefTypeCodec,
    ]
