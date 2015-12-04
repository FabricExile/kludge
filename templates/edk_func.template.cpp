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
{{ func.direct_result_edk_type }}
{{ func.edk_name }}(
    {{ func.edk_params }}
    )
{
    {% for param in func.params %}
    {{ param.edk_to_cpp }}
    {% endfor %}

    {{ func.edk_store_result_pre }}
    {{ func.cpp_name }}(
        {{ func.cpp_args }}
        ) {{ func.edk_store_result_post }};

    {% for param in func.params %}
    {{ param.cpp_to_edk }}
    {% endfor %}

    {{ func.edk_return_direct_result }}
}

//
//////////////////////////////////////////////////////////////////////////////
