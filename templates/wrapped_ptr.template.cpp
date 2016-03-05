//////////////////////////////////////////////////////////////////////////////
//
// KLUDGE EDK WrappedPtr
// {{ wrapped_ptr.desc }}
// {{ wrapped_ptr.location }}
//
//////////////////////////////////////////////////////////////////////////////
//

#include <{{ wrapped_ptr.include_filename }}>

namespace Fabric { namespace EDK { namespace KL {

struct {{ wrapped_ptr.name }} {
  ::{{ wrapped_ptr.name }} *cpp_ptr;
};

{% for member in wrapped_ptr.members %}
    {% if member.is_public %}
FABRIC_EXT_EXPORT
{{ member.codec.result_direct_type_edk() }}
{{ wrapped_ptr.name }}_GET_{{ member.codec.name.kl }}(
    {% set indirect_param_edk = member.codec.result_indirect_param_edk() %}
    {% if indirect_param_edk %}
      {{ indirect_param_edk | indent(4) }},
    {% endif %}
    {{ wrapped_ptr.self.param_edk() | indent(4) }}
    )
{
    {{ member.codec.result_indirect_init_edk() | indent(4) }}

    {{ member.codec.result_decl_and_assign_cpp() | indent(4) }}
        {{ wrapped_ptr.self.name.edk }}.cpp_ptr->{{ member.codec.name.kl }};

    {{ member.codec.result_indirect_assign_to_edk() | indent(4) }}
    {{ member.codec.result_direct_return_edk() | indent(4) }}
}
    
    {% endif %}
{% endfor %}

} } }

//
//////////////////////////////////////////////////////////////////////////////
