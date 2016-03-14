{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}

{% import "ast/builtin/macros.cpp" as macros %}
{% extends "ast/builtin/decl.template.cpp" %}
{% block body %}
namespace Fabric { namespace EDK { namespace KL {

typedef ::{{decl.this_type_info.lib.name.base}} {{decl.this_type_info.edk.name.local}}{{decl.this_type_info.lib.name.suffix}};

} } }

{% for method in decl.methods %}
FABRIC_EXT_EXPORT
{{method.result.render_direct_type_edk()}}
{{decl.this_type_info.kl.name.compound}}_{{method.name}}(
    {{macros.edk_param_list(method.result, method.this, method.params) | indent(4)}}
    )
{
    {{macros.cpp_call_pre(method.result, method.params) | indent(4)}}
        {{decl.this_value_name.edk}}.{{method.name}}(
            {{macros.cpp_call_args(method.params) | indent(12)}}
            );
    {{macros.cpp_call_post(method.result, method.params) | indent(4)}}
}
{% endfor %}
{% endblock body %}
