{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}

{% import "ast/builtin/macros.cpp" as macros %}
{% extends "ast/builtin/decl.template.cpp" %}
{% block body %}
{% for member in decl.members %}
    {% if member.is_public %}
FABRIC_EXT_EXPORT
{{member.result.render_direct_type_edk()}}
{{decl.this_type_info.kl.name.compound}}_GET_{{member.name}}(
    {% set indirect_param_edk = member.result.render_indirect_param_edk() %}
    {% if indirect_param_edk %}
      {{indirect_param_edk | indent(4)}},
    {% endif %}
    {{decl.const_this.render_param_edk() | indent(4)}}
    )
{
    {{member.result.render_indirect_init_edk() | indent(4)}}

    {{member.result.render_decl_and_assign_lib() | indent(4)}}
        {{decl.this_value_name.edk}}.cpp_ptr->{{member.name}};

    {{member.result.render_indirect_lib_to_edk() | indent(4) }}
    {{ member.result.render_direct_return_edk() | indent(4) }}
}

        {% if member.is_settable %}
FABRIC_EXT_EXPORT
void
{{decl.this_type_info.kl.name.compound}}_SET_{{member.name}}(
    {{decl.mutable_this.render_param_edk() | indent(4)}},
    {{ member.param.render_edk() | indent(4)}}
    )
{
    {{ member.param.render_edk_to_lib_decl() | indent(4) }}

    {{decl.this_value_name.edk}}.cpp_ptr->{{member.name}} =
        {{ member.param.render_lib() }};
}
        
        {% endif %}
    {% endif %}
{% endfor %}

{% if decl.block_empty_kl_constructor %}
FABRIC_EXT_EXPORT
void
{{decl.this_type_info.kl.name.compound}}_block_empty_constructor(
  {{decl.mutable_this.render_param_edk()}}
  )
{
  //::Fabric::EDK::throwException( "no empty constructor for {{decl.this_type_info.kl.name.compound}}" );
  {{decl.this_value_name.edk}}.cpp_ptr = 0;
}
{% endif %}

FABRIC_EXT_EXPORT
::Fabric::EDK::KL::Boolean
{{decl.this_type_info.kl.name.compound}}_is_null(
  {{decl.const_this.render_param_edk()}}
  )
{
  return {{decl.this_value_name.edk}}.cpp_ptr == 0;
}

{% for constructor in decl.constructors %}
//////////////////////////////////////////////////////////////////////////////
//
// KLUDGE EDK
// Description: {{ constructor.desc }}
// C++ Source Location: {{ constructor.location }}
//
//////////////////////////////////////////////////////////////////////////////
//
FABRIC_EXT_EXPORT
void
{{constructor.edk_symbol_name}}(
    {{macros.edk_param_list(constructor.result, constructor.this, constructor.params) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(constructor.result, constructor.params) | indent(4)}}
    {{decl.this_value_name.edk}}.cpp_ptr = new ::{{constructor.this.type_info.lib.name.base}}(
        {{macros.cpp_call_args(constructor.params) | indent(8)}}
        );
    {{macros.cpp_call_post(constructor.result, constructor.params) | indent(4)}}
}
//////////////////////////////////////////////////////////////////////////////

{% endfor %}

{% for method in decl.methods %}
//////////////////////////////////////////////////////////////////////////////
//
// KLUDGE EDK
// Description: {{ method.desc }}
// C++ Source Location: {{ method.location }}
//
//////////////////////////////////////////////////////////////////////////////
//
FABRIC_EXT_EXPORT
{{method.result.render_direct_type_edk()}}
{{method.edk_symbol_name}}(
    {{macros.edk_param_list(method.result, method.this, method.params) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(method.result, method.params) | indent(4)}}
        {{decl.this_value_name.edk}}.cpp_ptr->{{method.name}}(
            {{macros.cpp_call_args(method.params) | indent(12)}}
            );
    {{macros.cpp_call_post(method.result, method.params) | indent(4)}}
}
//////////////////////////////////////////////////////////////////////////////

{% endfor %}

{% endblock body %}
