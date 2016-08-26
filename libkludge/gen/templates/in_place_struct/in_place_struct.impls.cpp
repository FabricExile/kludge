{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% import "gen/macros.cpp" as macros %}
{% extends "gen/decl/decl.impls.cpp" %}
{% block body %}
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
    new (&{{decl.this_value_name.edk}}) {{constructor.name}}(
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
        {{decl.this_value_name.edk}}.{{method.name}}(
            {{macros.cpp_call_args(method.params) | indent(12)}}
            );
    {{macros.cpp_call_post(method.result, method.params) | indent(4)}}
}
//////////////////////////////////////////////////////////////////////////////

{% endfor %}
{% endblock body %}
