{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
{% import "generate/macros.cpp" as macros %}
{% extends "generate/decl/decl.impls.cpp" %}
{% block body %}
FABRIC_EXT_EXPORT
{{bin_op.result.render_direct_type_edk()}}
{{bin_op.get_edk_symbol_name()}}(
    {{macros.edk_param_list(bin_op.result, None, bin_op.params) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(bin_op.result, bin_op.params) | indent(4)}}
    operator{{bin_op.op | indent(4)}}(
        {{macros.cpp_call_args(bin_op.params)}}
        )
    {{macros.cpp_call_post(bin_op.result, bin_op.params) | indent(4)}}
}

{% endblock body %}
