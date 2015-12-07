//////////////////////////////////////////////////////////////////////////////
//
// KLUDGE EDK Function
// {{ func.desc }}
// {{ func.location }}
//
//////////////////////////////////////////////////////////////////////////////
//

#include <{{ func.include_filename }}>

FABRIC_EXT_EXPORT
{{ func.result_direct_type_edk() }}
{{ func.name_edk() }}(
    {{ func.params_edk() | indent(4) }}
    )
{
    {{ func.result_indirect_init_edk() | indent(4) }}

{% for param in func.params %}
    {{ param.param_edk_to_cpp_decl() | indent(4) }}
{% endfor %}

    {{ func.result_decl_and_assign_cpp() | indent(4) }}
    {{ func.name_cpp() | indent(4) }}(
        {{ func.params_cpp() | indent(8) }}
        );

{% for param in func.params %}
    {{ param.param_cpp_to_edk() | indent(4) }}
{% endfor %}

    {{ func.result_indirect_assign_to_edk() | indent(4) }}
    {{ func.result_direct_return_edk() | indent(4) }}
}

//
//////////////////////////////////////////////////////////////////////////////
