{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
{% if result.type_info.lib.name.base.endswith('&') %}
{{result.value_name.edk}}.cpp_ptr =
  reinterpret_cast< ::{{result.type_info.lib.name.base.partition('&')[0]}} * >(
    const_cast< ::{{result.type_info.lib.name.base.partition('&')[0]}} * >( &
{% else %}
{{result.value_name.edk}}.cpp_ptr =
  reinterpret_cast< ::{{result.type_info.lib.name.base}} >(
    const_cast< ::{{result.type_info.lib.name.base}} >(
{% endif %}
