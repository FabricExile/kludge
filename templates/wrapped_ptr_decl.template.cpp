{% import "macros.cpp" as macros %}
{% extends "decl.template.cpp" %}
{% block body %}
namespace Fabric { namespace EDK { namespace KL {

struct {{ decl.type.edk.local_name }} {
  ::{{ decl.type.cpp.name }} *cpp_ptr;
};

} } }

{% for member in decl.members %}
    {% if member.is_public %}
FABRIC_EXT_EXPORT
{{ member.codec.result_direct_type_edk() }}
{{ decl.type.kl.compound }}_GET_{{ member.codec.name.kl }}(
    {% set indirect_param_edk = member.codec.result_indirect_param_edk() %}
    {% if indirect_param_edk %}
      {{ indirect_param_edk | indent(4) }},
    {% endif %}
    {{ decl.self.param_edk() | indent(4) }}
    )
{
    {{ member.codec.result_indirect_init_edk() | indent(4) }}

    {{ member.codec.result_decl_and_assign_cpp() | indent(4) }}
        {{ decl.self.name.edk }}.cpp_ptr->{{ member.codec.name.kl }};

    {{ member.codec.result_indirect_assign_to_edk() | indent(4) }}
    {{ member.codec.result_direct_return_edk() | indent(4) }}
}
    
FABRIC_EXT_EXPORT
void
{{ decl.type.kl.compound }}_SET_{{ member.codec.name.kl }}(
    {{ decl.self.param_edk() | indent(4) }},
    {{ member.codec.param_edk() | indent(4)}}
    )
{
    {{ member.codec.param_edk_to_cpp_decl() | indent(4) }}

    {{ decl.self.name.edk }}.cpp_ptr->{{ member.codec.name.kl }} =
        {{ member.codec.param_cpp() }};
}
    
    {% endif %}
{% endfor %}

{% for method in decl.methods %}
FABRIC_EXT_EXPORT
{{ macros.edk_result_type(method.result_codec) }}
{{ decl.type.kl.compound }}_{{ method.name }}(
    {{ macros.edk_param_list(method.result_codec, decl.self, method.params) | indent(4) }}
    )
{
    {{ macros.cpp_call_pre(method.result_codec, method.params) | indent(4) }}
        {{ decl.self.name.edk }}.cpp_ptr->{{ method.name }}(
            {{ macros.cpp_call_args(method.params) | indent(12) }}
            );
    {{ macros.cpp_call_post(method.result_codec, method.params) | indent(4) }}
}
{% endfor %}

{% endblock body %}
