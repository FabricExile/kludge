{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}

{% import "ast/builtin/macros.cpp" as macros %}
{% extends "ast/builtin/decl.template.cpp" %}
{% block body %}
FABRIC_EXT_EXPORT
{{ decl.result_codec.render_direct_type_edk() }}
{{ decl.name_edk() }}(
    {{ macros.edk_param_list(decl.result_codec, None, decl.params) | indent(4) }}
    )
{
    {{ macros.cpp_call_pre(decl.result_codec, decl.params) | indent(4) }}
    {{ decl.name_cpp() | indent(4) }}(
        {{ macros.cpp_call_args(decl.params) }}
        );
    {{ macros.cpp_call_post(decl.result_codec, decl.params) | indent(4) }}
}
{% endblock body %}
