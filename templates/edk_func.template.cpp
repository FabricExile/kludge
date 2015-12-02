//////////////////////////////////////////////////////////////////////////////
//
// KLUDGE EDK Function
// {{ func.gen_desc() }}
// {{ func.gen_location() }}
//
//////////////////////////////////////////////////////////////////////////////
//

#include <{{ func.gen_include_filename() }}>

namespace Fabric { namespace EDK { namespace KL {

{{ func.gen_edk_dir_result_type() }}
{{ func.gen_edk_name() }}(
    {% for param in func.params %}
    {{ param.gen_edk_param(loop.last) }}
    {% endfor %}
    )
{
    {% for param in func.params %}
    {{ param.gen_edk_param_to_cpp_arg() }}
    {% endfor %}

    {{ func.gen_edk_store_result_pre() }}
    {{ func.gen_cpp_name() }}(
        {% for param in func.params %}
        {{ param.gen_cpp_arg(loop.last) }}
        {% endfor %}
        )
    {{ func.gen_edk_store_result_post() }}
    ;

    {% for param in func.params %}
    {{ param.gen_cpp_arg_to_edk_param() }}
    {% endfor %}

    {{ func.gen_edk_return_dir_result() }}
}

} } }

//
//////////////////////////////////////////////////////////////////////////////
