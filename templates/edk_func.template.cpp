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
    {{ func.params_edk() }}
    )
{
{% for param in func.params %}
    {{ param.param_edk_to_cpp() }}
{% endfor %}

    {{ func.result_decl_and_assign_cpp() }}
    {{ func.name_cpp() }}(
        {{ func.params_cpp() }}
        );

{% for param in func.params %}
    {{ param.param_cpp_to_edk() }}
{% endfor %}

    {{ func.result_indirect_assign_to_edk() }}
    {{ func.result_direct_return_edk() }}
}

//
//////////////////////////////////////////////////////////////////////////////
