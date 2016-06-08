{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}

{% if conv.type_info.lib.var_as_pointer %}
{{conv.value_name.lib}} = {{conv.value_name.edk}}.cpp_ptr;
{% else %}
{{conv.value_name.lib}} = *{{conv.value_name.edk}}.cpp_ptr;
{% endif %}
