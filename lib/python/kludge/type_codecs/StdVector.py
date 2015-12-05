from kludge import TypeSpec, TypeCodec, GenStr, GenLambda, SimpleTypeSpec, ValueName, Value
from kludge.CPPTypeExpr import *

def build_std_vector_type_codecs():

  def build_std_vector_type_spec(
    unqual_cpp_type_name,
    cpp_type_expr,
    element_type_info,
    ):
    return TypeSpec(
      element_type_info.spec.kl.base,
      '[]' + element_type_info.spec.kl.suffix,
      'VariableArray< ' + element_type_info.spec.edk.name + ' >',
      unqual_cpp_type_name,
      cpp_type_expr,
      [element_type_info],
      )

  def match_value(cpp_type_expr, type_mgr):
    if isinstance(cpp_type_expr, Template) \
      and cpp_type_expr.name == "std::vector":
        element_cpp_type_expr = cpp_type_expr.params[0]
        element_cpp_type_name = str(element_cpp_type_expr)
        element_type_info = type_mgr.maybe_get_type_info(element_cpp_type_name)
        if element_type_info:
          return build_std_vector_type_spec(
            'std::vector< ' + element_type_info.spec.cpp.qual_name + ' >',
            cpp_type_expr,
            element_type_info,
            )

  def match_const_ref(cpp_type_expr, type_mgr):
    if isinstance(cpp_type_expr, ReferenceTo) \
      and cpp_type_expr.pointee.is_const \
      and isinstance(cpp_type_expr.pointee, Template) \
      and cpp_type_expr.pointee.name == 'std::vector':
        element_cpp_type_expr = cpp_type_expr.pointee.params[0]
        element_cpp_type_name = str(element_cpp_type_expr)
        element_type_info = type_mgr.maybe_get_type_info(element_cpp_type_name)
        if element_type_info:
          return build_std_vector_type_spec(
            'std::vector< ' + element_type_info.spec.cpp.qual_name + ' >',
            cpp_type_expr,
            element_type_info,
            )

  return [
    TypeCodec(
      ).match(
        match_value
      ).traits_value(
      ).conv(
        edk_to_cpp = """
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
      ),
    TypeCodec(
      ).match(
        match_const_ref
      ).traits_const_ref(
      ).conv(
        edk_to_cpp = """
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
      ),
    ]
