{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% import "gen/macros.cpp" as macros %}
{% extends "gen/decl/decl.impls.cpp" %}
{% block body %}
{######################################################################}
{# Getters and Setters                                                #}
{######################################################################}
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
        {{record.const_this.render_member_ref(member.cpp_name) | indent(8)}};

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
{######################################################################}
{# Constructors and Destructor                                        #}
{######################################################################}
{% if record.include_empty_ctor %}
FABRIC_EXT_EXPORT void
{{record.empty_ctor_edk_symbol_name}}(
    {{macros.edk_param_list(None, record.mutable_this, None) | indent(4)}}
    )
{
    {{record.mutable_this.render_empty_ctor() | indent(4)}}
}

{% endif %}
{% if record.include_copy_ctor %}
FABRIC_EXT_EXPORT void
{{record.copy_ctor_edk_symbol_name}}(
    {{macros.edk_param_list(None, record.mutable_this, record.copy_params) | indent(4)}}
    )
{
    {{record.mutable_this.render_copy_ctor(record.copy_params[0]) | indent(4)}}
}

{% endif %}
{% for ctor in record.ctors %}
FABRIC_EXT_EXPORT void
{{ctor.edk_symbol_name}}(
    {{macros.edk_param_list(None, ctor.this, ctor.params) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(None, ctor.params) | indent(4)}}
    {{record.mutable_this.render_new_begin() | indent(4)}}
        {{macros.cpp_call_args(ctor.params) | indent(8)}}
        {{record.mutable_this.render_new_end() | indent(8)}}
    {{macros.cpp_call_post(None, ctor.params) | indent(4)}}
}

{% endfor %}
{% if record.include_dtor %}
FABRIC_EXT_EXPORT void
{{record.dtor_edk_symbol_name}}(
    {{record.mutable_this.render_param_edk()}}
    )
{
    {{record.mutable_this.render_delete()}}
}

{% endif %}
{######################################################################}
{# Methods                                                            #}
{######################################################################}
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
{# Unary Operators                                                    #}
{######################################################################}
{% for uni_op in record.uni_ops %}
FABRIC_EXT_EXPORT {{uni_op.result.render_direct_type_edk()}}
{{uni_op.edk_symbol_name}}(
    {{macros.edk_param_list(uni_op.result, uni_op.this, None) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(uni_op.result, None) | indent(4)}}
        {{uni_op.op}}{{uni_op.this.render_ref()}};
    {{macros.cpp_call_post(uni_op.result, None) | indent(4)}}
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
{% if record.include_simple_ass_op %}
FABRIC_EXT_EXPORT void
{{record.simple_ass_op_edk_symbol_name}}(
    {{macros.edk_param_list(None, record.mutable_this, record.copy_params) | indent(4)}}
    )
{
    {{record.mutable_this.render_simple_ass_op(record.copy_params[0]) | indent(4)}}
}

{% endif %}
{######################################################################}
{# Casts                                                              #}
{######################################################################}
{% for cast in record.casts %}
FABRIC_EXT_EXPORT void
{{cast.edk_symbol_name}}(
    {{macros.edk_param_list(None, cast.this, cast.params) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(None, cast.params) | indent(4)}}
    {{cast.this.render_new_begin() | indent(4)}}
        {{macros.cpp_call_args(cast.params) | indent(8)}}
        {{cast.this.render_new_end() | indent(8)}}
    {{macros.cpp_call_post(None, cast.params) | indent(4)}}
}

{% endfor %}
{######################################################################}
{# Index Operators                                                    #}
{######################################################################}
{% if record.get_ind_op_result %}
FABRIC_EXT_EXPORT {{record.get_ind_op_result.render_direct_type_edk()}}
{{record.get_ind_op_edk_symbol_name}}(
    {{macros.edk_param_list(record.get_ind_op_result, record.get_ind_op_this, record.get_ind_op_params) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(record.get_ind_op_result, record.get_ind_op_params) | indent(4)}}
        {{record.get_ind_op_this.render_ref() | indent(8)}}[
            {{record.get_ind_op_params[0].render_lib() | indent(12)}}
            ];
    {{macros.cpp_call_post(record.get_ind_op_result, record.get_ind_op_params) | indent(4)}}
}

{% endif %}
{% if record.set_ind_op_params %}
FABRIC_EXT_EXPORT void
{{record.set_ind_op_edk_symbol_name}}(
    {{macros.edk_param_list(None, record.set_ind_op_this, record.set_ind_op_params) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(None, record.set_ind_op_params) | indent(4)}}
    {{record.set_ind_op_this.render_ref() | indent(4)}}[
        {{record.set_ind_op_params[0].render_lib() | indent(8)}}
        ] = {{record.set_ind_op_params[1].render_lib() | indent(8)}};
    {{macros.cpp_call_post(None, record.set_ind_op_params) | indent(4)}}
}

{% endif %}
{% endblock body %}
