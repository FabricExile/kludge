{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
{% import "generate/macros.cpp" as macros %}
{% extends "generate/decl/decl.impls.cpp" %}
{% block body %}
{% if is_direct %}
{############################################################################}
{% if record.include_getters_setters %}

//////////////////////////////////////////////////////////////////////////////
// {{type_info}}
// Getters and Setters
//////////////////////////////////////////////////////////////////////////////
{% for member in record.members %}
{% if member.is_public() %}
{% if member.has_getter() %}

FABRIC_EXT_EXPORT
{{member.result.render_direct_type_edk()}}
{{member.get_getter_edk_symbol_name(type_info)}}(
    {% set indirect_param_edk = member.result.render_indirect_param_edk() %}
    {% if indirect_param_edk %}
      {{indirect_param_edk | indent(4)}},
    {% endif %}
    {{record.get_const_this(type_info).render_param_edk() | indent(4)}}
    )
{
    {{member.result.render_indirect_init_edk() | indent(4)}}

    {{member.result.render_decl_and_assign_lib_begin() | indent(4)}}
        {{record.get_const_this(type_info).render_member_ref(member.cpp_name) | indent(8)}}
        {{member.result.render_decl_and_assign_lib_end() | indent(4)}}

    {{member.result.render_indirect_lib_to_edk() | indent(4)}}
    {{member.result.render_direct_return_edk() | indent(4)}}
}
{% endif %}
{% if member.has_setter() and allow_mutable_methods %}

FABRIC_EXT_EXPORT void
{{member.get_setter_edk_symbol_name(type_info)}}(
    {{record.get_mutable_this(type_info).render_param_edk() | indent(4)}},
    {{member.param.render_edk() | indent(4)}}
    )
{
    {{member.param.render_edk_to_lib_decl() | indent(4)}}

    {{record.get_mutable_this(type_info).render_member_ref(member.cpp_name)}} =
        {{member.param.render_lib()}};
}
{% endif %}
{% endif %}
{% endfor %}
{% endif %}
{############################################################################}
{% if not is_direct or not record.is_abstract %}

//////////////////////////////////////////////////////////////////////////////
// {{type_info}}
// Constructors and Destructor
//////////////////////////////////////////////////////////////////////////////
{% if record.include_empty_ctor %}

FABRIC_EXT_EXPORT void
{{record.get_empty_ctor_edk_symbol_name(type_info)}}(
    {{macros.edk_param_list(None, record.get_mutable_this(type_info), None) | indent(4)}}
    )
{
    {{record.get_mutable_this(type_info).render_empty_ctor() | indent(4)}}
}
{% endif %}
{% if record.include_copy_ctor %}

FABRIC_EXT_EXPORT void
{{record.get_copy_ctor_edk_symbol_name(type_info)}}(
    {{macros.edk_param_list(None, record.get_mutable_this(type_info), [record.get_copy_param(type_info)]) | indent(4)}}
    )
{
    {{record.get_mutable_this(type_info).render_copy_ctor(record.get_copy_param(type_info)) | indent(4)}}
}
{% endif %}
{% for ctor in record.ctors %}

FABRIC_EXT_EXPORT void
{{ctor.get_edk_symbol_name(type_info)}}(
    {{macros.edk_param_list(None, ctor.get_this(type_info), ctor.params) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(None, ctor.params) | indent(4)}}
    {{record.get_mutable_this(type_info).render_new_begin() | indent(4)}}
        {{macros.cpp_call_args(ctor.params) | indent(8)}}
        {{record.get_mutable_this(type_info).render_new_end() | indent(8)}}
    {{macros.cpp_call_post(None, ctor.params) | indent(4)}}
}
{% endfor %}
{% if record.include_dtor %}

FABRIC_EXT_EXPORT void
{{record.get_dtor_edk_symbol_name(type_info)}}(
    {{record.get_mutable_this(type_info).render_param_edk()}}
    )
{
    {{record.get_mutable_this(type_info).render_delete()}}
}
{% endif %}
{% endif %}
{############################################################################}
{% if record.has_methods %}

//////////////////////////////////////////////////////////////////////////////
// {{type_info}}
// Methods
//////////////////////////////////////////////////////////////////////////////
{% for method in record.methods %}
{% if (method.is_static and allow_static_methods)
    or (method.is_mutable and allow_mutable_methods)
    or (method.is_const and allow_const_methods) %}

FABRIC_EXT_EXPORT {{method.result.render_direct_type_edk()}}
{{method.get_edk_symbol_name(type_info)}}(
{% if method.is_static %}
    {{macros.edk_param_list(method.result, None, method.params) | indent(4)}}
{% else %}
    {{macros.edk_param_list(method.result, method.get_this(type_info), method.params) | indent(4)}}
{% endif %}
    )
{
    {{macros.cpp_call_pre(method.result, method.params) | indent(4)}}

{% if method.is_static %}
    {{record.get_mutable_this(type_info).render_class_name_cpp()}}::{{method.cpp_name}}(
{% else %}
    {{method.get_this(type_info).render_member_ref(method.cpp_name)}}(
{% endif %}
        {{macros.cpp_call_args(method.params) | indent(8)}}
        )
    {{macros.cpp_call_post(method.result, method.params) | indent(4)}}
}
{% endif %}
{% endfor %}
{% endif %}
{############################################################################}
{% if record.has_call_ops %}

//////////////////////////////////////////////////////////////////////////////
// {{type_info}}
// call_ops
//////////////////////////////////////////////////////////////////////////////
{% for call_op in record.call_ops %}
{% if (call_op.is_mutable and allow_mutable_methods)
    or (call_op.is_const and allow_const_methods) %}

FABRIC_EXT_EXPORT {{call_op.result.render_direct_type_edk()}}
{{call_op.get_edk_symbol_name(type_info)}}(
{% if call_op.is_static %}
    {{macros.edk_param_list(call_op.result, None, call_op.params) | indent(4)}}
{% else %}
    {{macros.edk_param_list(call_op.result, call_op.get_this(type_info), call_op.params) | indent(4)}}
{% endif %}
    )
{
    {{macros.cpp_call_pre(call_op.result, call_op.params) | indent(4)}}

    {{call_op.get_this(type_info).render_ref()}}(
        {{macros.cpp_call_args(call_op.params) | indent(8)}}
        )
    {{macros.cpp_call_post(call_op.result, call_op.params) | indent(4)}}
}
{% endif %}
{% endfor %}
{% endif %}
{############################################################################}
{% if record.has_uni_ops() %}

//////////////////////////////////////////////////////////////////////////////
// {{type_info}}
// Unary Operators
//////////////////////////////////////////////////////////////////////////////
{% for uni_op in record.uni_ops %}

FABRIC_EXT_EXPORT {{uni_op.result.render_direct_type_edk()}}
{{uni_op.get_edk_symbol_name(type_info)}}(
    {{macros.edk_param_list(uni_op.result, uni_op.get_this(type_info), None) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(uni_op.result, None) | indent(4)}}
        {{uni_op.op}}{{uni_op.get_this(type_info).render_ref()}}
    {{macros.cpp_call_post(uni_op.result, None) | indent(4)}}
}
{% endfor %}
{% endif %}
{############################################################################}
{% if record.has_bin_ops() %}

//////////////////////////////////////////////////////////////////////////////
// {{type_info}}
// Binary Operators
//////////////////////////////////////////////////////////////////////////////
{% for bin_op in record.bin_ops %}

FABRIC_EXT_EXPORT {{bin_op.result.render_direct_type_edk()}}
{{bin_op.get_edk_symbol_name(type_info)}}(
    {{macros.edk_param_list(bin_op.result, None, bin_op.params) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(bin_op.result, bin_op.params) | indent(4)}}
        {{macros.cpp_call_args([bin_op.params[0]]) | indent(8)}} {{bin_op.op}}
            {{macros.cpp_call_args([bin_op.params[1]]) | indent(12)}}
    {{macros.cpp_call_post(bin_op.result, bin_op.params) | indent(4)}}
}
{% endfor %}
{% endif %}
{############################################################################}
{% if not record.is_abstract and record.include_simple_ass_op %}

//////////////////////////////////////////////////////////////////////////////
// {{type_info}}
// Simple Assignment Operator
//////////////////////////////////////////////////////////////////////////////

FABRIC_EXT_EXPORT void
{{record.get_simple_ass_op_edk_symbol_name(type_info)}}(
    {{macros.edk_param_list(None, record.get_mutable_this(type_info), [record.get_copy_param(type_info)]) | indent(4)}}
    )
{
    {{record.get_mutable_this(type_info).render_simple_ass_op(record.get_copy_param(type_info)) | indent(4)}}
}
{% endif %}
{############################################################################}
{% if not record.is_abstract and record.has_ass_ops() %}

//////////////////////////////////////////////////////////////////////////////
// {{type_info}}
// Other Assignment Operators
//////////////////////////////////////////////////////////////////////////////
{% for ass_op in record.ass_ops %}

FABRIC_EXT_EXPORT void
{{ass_op.get_edk_symbol_name(type_info)}}(
    {{macros.edk_param_list(None, ass_op.get_this(type_info), ass_op.params) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(None, ass_op.params) | indent(4)}}
    {{ass_op.get_this(type_info).render_ref()}} {{ass_op.op}}
        {{macros.cpp_call_args(ass_op.params) | indent(8)}}
    {{macros.cpp_call_post(None, ass_op.params) | indent(4)}}
}
{% endfor %}
{% endif %}
{############################################################################}
{% if record.has_casts() %}

//////////////////////////////////////////////////////////////////////////////
// {{type_info}}
// Casts
//////////////////////////////////////////////////////////////////////////////
{% for cast in record.casts %}

FABRIC_EXT_EXPORT void
{{cast.get_edk_symbol_name(type_info)}}(
    {{macros.edk_param_list(None, cast.this, cast.get_params(type_info)) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(None, cast.get_params(type_info)) | indent(4)}}
    {{cast.this.render_new_begin() | indent(4)}}
        {{macros.cpp_call_args(cast.get_params(type_info)) | indent(8)}}
        {{cast.this.render_new_end() | indent(8)}}
    {{macros.cpp_call_post(None, cast.get_params(type_info)) | indent(4)}}
}
{% endfor %}
{% endif %}
{############################################################################}
{% if record.const_deref_kl_method_name %}

//////////////////////////////////////////////////////////////////////////////
// {{type_info}}
// ConstDeref
//////////////////////////////////////////////////////////////////////////////

FABRIC_EXT_EXPORT {{record.const_deref_result.render_direct_type_edk()}}
{{record.get_const_deref_edk_symbol_name(type_info)}}(
    {{macros.edk_param_list(record.const_deref_result, record.get_const_deref_this(type_info), None) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(record.const_deref_result, None) | indent(4)}}
        *{{record.get_const_deref_this(type_info).render_ref() | indent(8)}}
    {{macros.cpp_call_post(record.const_deref_result, None) | indent(4)}}
}
{% endif %}
{############################################################################}
{% if record.mutable_deref_kl_method_name %}

//////////////////////////////////////////////////////////////////////////////
// {{type_info}}
// MutableDeref
//////////////////////////////////////////////////////////////////////////////

FABRIC_EXT_EXPORT {{record.mutable_deref_result.render_direct_type_edk()}}
{{record.get_mutable_deref_edk_symbol_name(type_info)}}(
    {{macros.edk_param_list(record.mutable_deref_result, record.get_mutable_deref_this(type_info), None) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(record.mutable_deref_result, None) | indent(4)}}
        *{{record.get_mutable_deref_this(type_info).render_ref() | indent(8)}}
    {{macros.cpp_call_post(record.mutable_deref_result, None) | indent(4)}}
}
{% endif %}
{############################################################################}
{% if record.get_ind_op_result %}

//////////////////////////////////////////////////////////////////////////////
// {{type_info}}
// cxxGetAtIndex(Index) Operator
//////////////////////////////////////////////////////////////////////////////

FABRIC_EXT_EXPORT {{record.get_ind_op_result.render_direct_type_edk()}}
{{record.get_get_ind_op_edk_symbol_name(type_info)}}(
    {{macros.edk_param_list(record.get_ind_op_result, record.get_get_ind_op_this(type_info), record.get_ind_op_params) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(record.get_ind_op_result, record.get_ind_op_params) | indent(4)}}
        {{record.get_get_ind_op_this(type_info).render_ref() | indent(8)}}[
            {{record.get_ind_op_params[0].render_lib() | indent(12)}}
            ]
    {{macros.cpp_call_post(record.get_ind_op_result, record.get_ind_op_params) | indent(4)}}
}
{% endif %}
{############################################################################}
{% if record.set_ind_op_params and allow_mutable_methods %}

//////////////////////////////////////////////////////////////////////////////
// {{type_info}}
// cxxSetAtIndex(Index) Operator
//////////////////////////////////////////////////////////////////////////////

FABRIC_EXT_EXPORT void
{{record.get_set_ind_op_edk_symbol_name(type_info)}}(
    {{macros.edk_param_list(None, record.get_set_ind_op_this(type_info), record.set_ind_op_params) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(None, record.set_ind_op_params) | indent(4)}}
    {{record.get_set_ind_op_this(type_info).render_ref() | indent(4)}}[
        {{record.set_ind_op_params[0].render_lib() | indent(8)}}
        ] = {{record.set_ind_op_params[1].render_lib() | indent(8)}}
    {{macros.cpp_call_post(None, record.set_ind_op_params) | indent(4)}}
}
{% endif %}
{############################################################################}
{% endif %}
{% endblock body %}
