{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% import "gen/macros.cpp" as macros %}
{% extends "gen/decl/decl.impls.cpp" %}
{% block body %}
{% if record.include_getters_setters %}
{% for member in record.members %}
{% if member.is_public() %}
{% if member.has_getter() %}
FABRIC_EXT_EXPORT
{{member.result.render_direct_type_edk()}}
{{record.this_type_info.kl.name.compound}}_GET_{{member.cpp_name}}(
    {% set indirect_param_edk = member.result.render_indirect_param_edk() %}
    {% if indirect_param_edk %}
      {{indirect_param_edk | indent(4)}},
    {% endif %}
    {{record.const_this.render_param_edk() | indent(4)}}
    )
{
    {{member.result.render_indirect_init_edk() | indent(4)}}

    {{member.result.render_decl_and_assign_lib() | indent(4)}}
        {{record.const_this.render_member_ref(member.cpp_name)}};

    {{member.result.render_indirect_lib_to_edk() | indent(4)}}
    {{member.result.render_direct_return_edk() | indent(4)}}
}

{% endif %}
{% if member.has_setter() %}
FABRIC_EXT_EXPORT void
{{record.this_type_info.kl.name.compound}}_SET_{{member.cpp_name}}(
    {{record.mutable_this.render_param_edk() | indent(4)}},
    {{member.param.render_edk() | indent(4)}}
    )
{
    {{member.param.render_edk_to_lib_decl() | indent(4)}}

    {{record.mutable_this.render_member_ref(member.cpp_name)}} =
        {{member.param.render_lib()}};
}
        
{% endif %}
{% endif %}
{% endfor %}
{% endif %}
{% for ctor in record.ctors %}
FABRIC_EXT_EXPORT void
{{ctor.edk_symbol_name}}(
    {{macros.edk_param_list(ctor.result, ctor.this, ctor.params) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(ctor.result, ctor.params) | indent(4)}}
    {{record.mutable_this.render_new_begin() | indent(4)}}
        {{macros.cpp_call_args(ctor.params) | indent(8)}}
        {{record.mutable_this.render_new_end() | indent(8)}}
    {{macros.cpp_call_post(ctor.result, ctor.params) | indent(4)}}
}

{% endfor %}
{% if record.include_dtor %}
FABRIC_EXT_EXPORT void
{{record.dtor_edk_symbol_name}}(
    {{record.mutable_this.render_param_edk()}}
    )
{
    {{record.mutable_this.render_delete()}};
}

{% endif %}
{% for method in record.methods %}
FABRIC_EXT_EXPORT {{method.result.render_direct_type_edk()}}
{{method.edk_symbol_name}}(
{% if method.is_static %}
    {{macros.edk_param_list(method.result, None, method.params) | indent(4)}}
{% else %}
    {{macros.edk_param_list(method.result, method.this, method.params) | indent(4)}}
{% endif %}
    )
{
    {{macros.cpp_call_pre(method.result, method.params) | indent(4)}}

{% if method.is_static %}
    {{method.this.render_class_name()}}::{{method.cpp_name}}(
{% else %}
    {{method.this.render_member_ref(method.cpp_name)}}(
{% endif %}
        {{macros.cpp_call_args(method.params) | indent(8)}}
        );
    {{macros.cpp_call_post(method.result, method.params) | indent(4)}}
}

{% endfor %}
{######################################################################}
{# Binary Operators                                                   #}
{######################################################################}
{% for bin_op in record.bin_ops %}
FABRIC_EXT_EXPORT {{bin_op.result.render_direct_type_edk()}}
{{bin_op.edk_symbol_name}}(
    {{macros.edk_param_list(bin_op.result, None, bin_op.params) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(bin_op.result, bin_op.params) | indent(4)}}
        {{macros.cpp_call_args([bin_op.params[0]]) | indent(8)}} {{bin_op.op}}
            {{macros.cpp_call_args([bin_op.params[1]]) | indent(12)}};
    {{macros.cpp_call_post(bin_op.result, bin_op.params) | indent(4)}}
}

{% endfor %}
{######################################################################}
{# Assignment Operators                                               #}
{######################################################################}
{% for ass_op in record.ass_ops %}
FABRIC_EXT_EXPORT void
{{ass_op.edk_symbol_name}}(
    {{macros.edk_param_list(None, ass_op.this, ass_op.params) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(None, ass_op.params) | indent(4)}}
    {{ass_op.this.render_ref()}} {{ass_op.op}}
        {{macros.cpp_call_args(ass_op.params) | indent(8)}};
    {{macros.cpp_call_post(None, ass_op.params) | indent(4)}}
}

{% endfor %}

{% endblock body %}
