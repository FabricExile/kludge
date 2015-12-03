//////////////////////////////////////////////////////////////////////////////
//
// KLUDGE EDK Function
// {{ func.gen_desc() }}
// {{ func.gen_location() }}
//
//////////////////////////////////////////////////////////////////////////////
//

#include <{{ func.gen_include_filename() }}>

FABRIC_EXT_EXPORT
{{ func.gen_direct_result_edk_type() }}
{{ func.gen_edk_name() }}(
    {{ func.gen_edk_params() }}
    )
{
    {% for param in func.params %}
    {{ param.gen_edk_to_cpp() }}
    {% endfor %}

    {{ func.gen_edk_store_result_pre() }}
    {{ func.gen_cpp_name() }}(
        {{ func.gen_cpp_args() }}
        ) {{ func.gen_edk_store_result_post() }};

    {% for param in func.params %}
    {{ param.gen_cpp_to_edk() }}
    {% endfor %}

    {{ func.gen_edk_return_dir_result() }}
}

//
//////////////////////////////////////////////////////////////////////////////
