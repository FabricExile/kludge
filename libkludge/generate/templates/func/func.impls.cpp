{######################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% import "generate/macros.cpp" as macros %}
{% extends "generate/decl/decl.impls.cpp" %}
{% block body %}
FABRIC_EXT_EXPORT
{{func.result.render_direct_type_edk()}}
{{func.get_edk_symbol_name()}}(
    {{macros.edk_param_list(func.result, None, func.params) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(func.result, func.params) | indent(4)}}
    {{func.cpp_global_name | indent(4)}}(
        {{macros.cpp_call_args(func.params)}}
        )
    {{macros.cpp_call_post(func.result, func.params) | indent(4)}}
}

{% endblock body %}
