from kludge import TypeSpec, TypeCodec, GenStr, GenLambda, SimpleTypeSpec, ValueName, Value
from kludge.CPPTypeExpr import *

def build_std_vector_type_codecs(jinjenv):
  def build_std_vector_type_spec(
    cpp_type_spec,
    element_type_info,
    ):
    return TypeSpec(
      element_type_info.spec.kl.base,
      '[]' + element_type_info.spec.kl.suffix,
      'VariableArray< ' + element_type_info.spec.edk.name + ' >',
      cpp_type_spec,
      [Value(ValueName("RESERVED_element"), element_type_info)],
      )

  def match_value_or_const_ref(cpp_type_spec, type_mgr):
    cpp_type_expr = cpp_type_spec.expr
    if isinstance(cpp_type_expr, Template) \
      and cpp_type_expr.name == "std::vector":
        element_cpp_type_expr = cpp_type_expr.params[0]
        element_cpp_type_name = str(element_cpp_type_expr)
        element_type_info = type_mgr.maybe_get_type_info(element_cpp_type_name)
        if element_type_info:
          return build_std_vector_type_spec(
            cpp_type_spec,
            element_type_info,
            )
    if isinstance(cpp_type_expr, ReferenceTo) \
      and cpp_type_expr.pointee.is_const \
      and isinstance(cpp_type_expr.pointee, Template) \
      and cpp_type_expr.pointee.name == 'std::vector':
        element_cpp_type_expr = cpp_type_expr.pointee.params[0]
        element_cpp_type_name = str(element_cpp_type_expr)
        element_type_info = type_mgr.maybe_get_type_info(element_cpp_type_name)
        if element_type_info:
          return build_std_vector_type_spec(
            cpp_type_spec,
            element_type_info,
            )

  return [
    TypeCodec(
      jinjenv
      ).match(
        match_value_or_const_ref
      ).no_result(
      ).in_param(
      ).conv(
        edk_to_cpp = """
std::vector< {{ element.cpp.name }} > {{ name.cpp }};
{{ name.cpp }}.reserve( {{ name.edk }}.size() );
for ( uint32_t i = 0; i < {{ name.edk }}.size(); ++i )
{
  {{ element.edk_to_cpp() }}
  {{ name.cpp }}.push_back( {{ element.cpp_arg }} );
}
""",
        cpp_arg = GenLambda(
          lambda gd: gd.name.cpp
          ),
        cpp_to_edk = GenStr(""),
      ),
    ]
