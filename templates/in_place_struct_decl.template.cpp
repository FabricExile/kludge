{% import "macros.cpp" as macros %}
{% extends "decl.template.cpp" %}
{% block body %}
namespace Fabric { namespace EDK { namespace KL {

typedef {{ decl.self_type_name.cpp.name }} {{ decl.self_type_name.edk.local_name }};

} } }

{% for method in decl.methods %}
  {% if method.is_const %}
    {% set self_codec = decl.self_codec_const %}
  {% else %}
    {% set self_codec = decl.self_codec_mutable %}
  {% endif %}
FABRIC_EXT_EXPORT
{{ macros.edk_result_type(method.result_codec) }}
{{ decl.self_type_name.kl.compound }}_{{ method.name }}(
    {{ macros.edk_param_list(method.result_codec, self_codec, method.params) | indent(4) }}
    )
{
    {{ macros.cpp_call_pre(method.result_codec, method.params) | indent(4) }}
        {{ self_codec.name.edk }}.{{ method.name }}(
            {{ macros.cpp_call_args(method.params) | indent(12) }}
            );
    {{ macros.cpp_call_post(method.result_codec, method.params) | indent(4) }}
}
{% endfor %}
{% endblock body %}
