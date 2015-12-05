from kludge import TypeSpec, TypeCodec, GenStr, GenLambda, SimpleTypeSpec, ValueName, Value
from kludge.CPPTypeExpr import *
from kludge.CPPTypeExpr.helpers import *

def build_std_map_type_codecs():

  def build_std_map_type_spec(
    unqual_cpp_type_name,
    cpp_type_expr,
    key_type_info,
    value_type_info,
    ):
    return TypeSpec(
      value_type_info.kl.base,
      '[' + key_type_info.kl.compound + ']' + value_type_info.kl.suffix,
      'Dict< ' + key_type_info.edk.name + ', ' + value_type_info.edk.name + ' >',
      unqual_cpp_type_name,
      cpp_type_expr,
      [key_type_info, value_type_info],
      )

  class StdMapTypeCodecBase(TypeCodec): pass
  StdMapTypeCodecBase.conv(
    edk_to_cpp = """
{{ name.cpp }}.clear();
for ( {{ type.edk.name }}::CIT it = {{ name.edk }}.begin();
  it != {{ name.edk }}.end(); ++it )
{
    {{ children[0].type.edk.name }} const &{{ children[0].name.edk }} = it.key();
    {{ children[0].conv_edk_to_cpp_decl() }}
    {{ children[1].type.edk.name }} const &{{ children[1].name.edk }} = it.value();
    {{ children[1].conv_edk_to_cpp_decl() }}
    {{ name.cpp }}[{{ children[0].name.cpp }}] = {{ children[1].name.cpp }};
}
""",
    edk_to_cpp_decl = GenLambda(
      lambda gd: gd.type.cpp.name + " " + gd.name.cpp + ";\n    " + gd.conv_edk_to_cpp()
      ),
    cpp_to_edk = """
// {{ name.edk }}.clear();
for ( {{ type.cpp.name }}::const_iterator it = {{ name.cpp }}.begin();
  it != {{ name.cpp }}.end(); ++it )
{
    {{ children[0].type.cpp.name }} const &{{ children[0].name.cpp }} = {{ children[0].traits_pointer_undo() }}it->first;
    {{ children[0].conv_cpp_to_edk_decl() }}
    {{ children[1].type.cpp.name }} const &{{ children[1].name.cpp }} = {{ children[1].traits_pointer_undo() }}it->second;
    {{ children[1].conv_cpp_to_edk_decl() }}
    {{ name.edk }}[{{ children[0].name.edk }}] = {{ children[1].name.edk }};
}
""",
    cpp_to_edk_decl = GenLambda(
      lambda gd: gd.type.edk.name + " " + gd.name.edk + ";\n    " + gd.conv_cpp_to_edk()
      ),
    )

  def is_std_map(cpp_type_expr):
    return isinstance(cpp_type_expr, Template) \
      and cpp_type_expr.name == "std::map"

  def match_value(cls, cpp_type_expr, type_mgr):
    if is_std_map(cpp_type_expr):
      key_cpp_type_expr = cpp_type_expr.params[0]
      key_type_info = type_mgr.maybe_get_type_info(key_cpp_type_expr)
      if key_type_info:
        value_cpp_type_expr = cpp_type_expr.params[1]
        value_type_info = type_mgr.maybe_get_type_info(value_cpp_type_expr)
        if value_type_info:
          return build_std_map_type_spec(
            'std::map< ' + key_type_info.cpp.qual_name + ', ' + value_type_info.cpp.qual_name + ' >',
            cpp_type_expr,
            key_type_info,
            value_type_info,
            )

  class StdMapValueTypeCodec(StdMapTypeCodecBase): pass
  StdMapValueTypeCodec.match(match_value)
  StdMapValueTypeCodec.traits_value()

  def match_const_ref(cls, cpp_type_expr, type_mgr):
    if is_const_ref(cpp_type_expr):
      base_cpp_type_expr = cpp_type_expr.pointee
      if is_std_map(base_cpp_type_expr):
        key_cpp_type_expr = base_cpp_type_expr.params[0]
        key_type_info = type_mgr.maybe_get_type_info(key_cpp_type_expr)
        if key_type_info:
          value_cpp_type_expr = base_cpp_type_expr.params[1]
          value_type_info = type_mgr.maybe_get_type_info(value_cpp_type_expr)
          if value_type_info:
            return build_std_map_type_spec(
              'std::map< ' + key_type_info.cpp.qual_name + ', ' + value_type_info.cpp.qual_name + ' >',
              cpp_type_expr,
              key_type_info,
              value_type_info,
              )

  class StdMapConstRefTypeCodec(StdMapTypeCodecBase): pass
  StdMapConstRefTypeCodec.match(match_const_ref)
  StdMapConstRefTypeCodec.traits_const_ref()

  return [
    StdMapValueTypeCodec,
    StdMapConstRefTypeCodec,
    ]
