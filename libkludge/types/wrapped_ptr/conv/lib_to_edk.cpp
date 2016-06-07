{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}

{% if conv.is_pointer %}
{{conv.value_name.edk}}.cpp_ptr = &{{conv.value_name.lib}};
{% else %}
delete {{conv.value_name.edk}}.cpp_ptr;
{{conv.value_name.edk}}.cpp_ptr = new {{conv.type_info.lib.name.compound}}( {{conv.value_name.lib}} );
{% endif %}
