{% import "macros.cpp" as macros %}
{% extends "decl.template.cpp" %}
{% block body %}
FABRIC_EXT_EXPORT
{{ macros.edk_result_type(decl.result_codec) }}
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
