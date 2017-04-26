{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
{% if conv.type_info.lib.name.base.endswith('&') %}
{{conv.value_name.lib}} = * reinterpret_cast< ::{{conv.type_info.lib.name.base.partition('&')[0]}} * >( {{conv.value_name.edk}}.cpp_ptr );
{% else %}
{{conv.value_name.lib}} = reinterpret_cast< ::{{conv.type_info.lib.name.base}} >( {{conv.value_name.edk}}.cpp_ptr );
{% endif %}
