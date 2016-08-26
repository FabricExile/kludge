{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% import "gen/macros.cpp" as macros %}
{% extends "gen/decl/decl.impls.cpp" %}
{% block body %}
{% for member in decl.members %}
{% if member.has_getter() %}
FABRIC_EXT_EXPORT
{{member.result.render_direct_type_edk()}}
{{decl.this_type_info.kl.name.compound}}_GET_{{member.cpp_name}}(
    {% set indirect_param_edk = member.result.render_indirect_param_edk() %}
    {% if indirect_param_edk %}
      {{indirect_param_edk | indent(4)}},
    {% endif %}
    {{decl.const_this.render_param_edk() | indent(4)}}
    )
{
    {{member.result.render_indirect_init_edk() | indent(4)}}

    {{member.result.render_decl_and_assign_lib() | indent(4)}}
        {{decl.this_value_name.edk}}.cpp_ptr->{{member.cpp_name}};

    {{member.result.render_indirect_lib_to_edk() | indent(4)}}
    {{member.result.render_direct_return_edk() | indent(4)}}
}

{% endif %}
{% if member.has_setter() %}
FABRIC_EXT_EXPORT void
{{decl.this_type_info.kl.name.compound}}_SET_{{member.cpp_name}}(
    {{decl.mutable_this.render_param_edk() | indent(4)}},
    {{member.param.render_edk() | indent(4)}}
    )
{
    {{member.param.render_edk_to_lib_decl() | indent(4)}}

    {{decl.this_value_name.edk}}.cpp_ptr->{{member.cpp_name}} =
        {{member.param.render_lib()}};
}
        
{% endif %}
{% endfor %}
{% for ctor in decl.ctors %}
FABRIC_EXT_EXPORT
void
{{ctor.edk_symbol_name}}(
    {{macros.edk_param_list(ctor.result, ctor.this, ctor.params) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(ctor.result, ctor.params) | indent(4)}}
    {{decl.this_value_name.edk}}.cpp_ptr = new ::{{ctor.this.type_info.lib.name.base}}(
        {{macros.cpp_call_args(ctor.params) | indent(8)}}
        );
    {{macros.cpp_call_post(ctor.result, ctor.params) | indent(4)}}
}

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

    {% if method.uses_operator_arrow %}
        ( *{{decl.this_value_name.edk}}.cpp_ptr )->{{method.name}}(
    {% else %}
        {{decl.this_value_name.edk}}.cpp_ptr->{{method.name}}(
    {% endif %}
            {{macros.cpp_call_args(method.params) | indent(12)}}
            );
    {{macros.cpp_call_post(method.result, method.params) | indent(4)}}
}
//////////////////////////////////////////////////////////////////////////////

{% endfor %}

{% endblock body %}
