{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}

{% if conv.type_info.lib.var_as_pointer or conv.is_pointer %}
{{conv.type_info.edk.name.toplevel}} *{{conv.value_name.edk}};
{{conv.value_name.edk}}.cpp_ptr = {{conv.value_name.lib}};
{% else %}
{{conv.type_info.edk.name.toplevel}} {{conv.value_name.edk}};
{{conv.value_name.edk}}.cpp_ptr = new {{conv.type_info.lib.name.compound}}( {{conv.value_name.lib}} );
{% endif %}
