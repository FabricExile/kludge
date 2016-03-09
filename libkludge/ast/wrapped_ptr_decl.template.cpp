{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}

{% import "ast/builtin/macros.cpp" as macros %}
{% extends "ast/builtin/decl.template.cpp" %}
{% block body %}
namespace Fabric { namespace EDK { namespace KL {

struct {{decl.this_type_info.edk.name.local}} {
  ::{{decl.this_type_info.lib.name}} *cpp_ptr;
};

} } }

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

{% for method in decl.methods %}
FABRIC_EXT_EXPORT
{{method.result.render_direct_type_edk()}}
{{decl.this_type_info.kl.name.compound}}_{{method.name}}(
    {{macros.edk_param_list(method.result, method.this, method.params) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(method.result, method.params) | indent(4)}}
        {{decl.this_value_name.edk}}.cpp_ptr->{{method.name}}(
            {{macros.cpp_call_args(method.params) | indent(12)}}
            );
    {{macros.cpp_call_post(method.result, method.params) | indent(4)}}
}
{% endfor %}

{% endblock body %}
