{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% import "gen/macros.cpp" as macros %}
{% extends "gen/decl/decl.impls.cpp" %}
{% block body %}
FABRIC_EXT_EXPORT
{{func.result_codec.render_direct_type_edk()}}
{{func.edk_symbol_name}}(
    {{macros.edk_param_list(func.result_codec, None, func.params) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(func.result_codec, func.params) | indent(4)}}
    {{func.name_cpp | indent(4)}}(
        {{macros.cpp_call_args(func.params)}}
        );
    {{macros.cpp_call_post(func.result_codec, func.params) | indent(4)}}
}

{% endblock body %}
