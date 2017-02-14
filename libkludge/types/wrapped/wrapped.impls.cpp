{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
{% extends "generate/decl/decl.impls.cpp" %}
{% block body %}
{{decl.render_method_impls('cpp')}}
FABRIC_EXT_EXPORT Fabric::EDK::KL::UInt64
{{decl.type_info.cxx_size_func_name}}()
{
  return sizeof({{decl.type_info.lib.name}});
}

FABRIC_EXT_EXPORT void
{{decl.rawToWrapped_edk_symbol_name()}}(
  ::Fabric::EDK::KL::Traits< {{decl.wrapped_type_info.edk.name}} >::IOParam wrapped,
  ::Fabric::EDK::KL::Traits< {{decl.raw_type_info.edk.name}} >::INParam raw
  )
{
  if ( raw.cpp_ptr )
    wrapped.cpp_ptr =
      new ::{{decl.wrapped_type_info.base_type_info.lib.name.base}}(
        static_cast< ::{{decl.wrapped_type_info.lib.expr.components[0].params[0]}} * >(
          raw.cpp_ptr
          )
        );
  else
    wrapped.cpp_ptr = NULL;
}

FABRIC_EXT_EXPORT void
{{decl.wrappedToRaw_edk_symbol_name()}}(
  ::Fabric::EDK::KL::Traits< {{decl.raw_type_info.edk.name}} >::IOParam raw,
  ::Fabric::EDK::KL::Traits< {{decl.type_info.edk.name}} >::INParam wrapped
  )
{
  if ( wrapped.cpp_ptr )
    raw.cpp_ptr = wrapped.cpp_ptr->operator->();
  else
    raw.cpp_ptr = NULL;
}

{% endblock body %}
