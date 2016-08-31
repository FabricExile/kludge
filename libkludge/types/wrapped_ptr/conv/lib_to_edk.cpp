{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}

{% if conv.type_info.lib.var_as_pointer or conv.is_mutable_pointer %}
{{conv.value_name.edk}}.cpp_ptr = {{conv.value_name.lib}};
{% elif conv.is_pointer and not conv.is_mutable_pointer %}
{{conv.value_name.edk}}.cpp_ptr = const_cast<{{conv.type_info.lib.name.base}} *>( {{conv.value_name.lib}} );
{% elif conv.is_mutable_reference %}
{{conv.value_name.edk}}.cpp_ptr = &{{conv.value_name.lib}};
{% elif conv.is_reference and not conv.is_mutable_reference %}
{{conv.value_name.edk}}.cpp_ptr = const_cast<{{conv.type_info.lib.name.base}} *>( &{{conv.value_name.lib}} );
{% else %}
delete {{conv.value_name.edk}}.cpp_ptr;
{{conv.value_name.edk}}.cpp_ptr = new {{conv.type_info.lib.name.compound}}( {{conv.value_name.lib}} );
{% endif %}
