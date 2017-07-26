{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
{% if this.type_info.is_direct %}
{{this.value_name.edk}} = {{param.value_name.edk}};
{% else %}
{%   if this.type_info.lib.name.base.endswith('&') %}
{{this.value_name.edk}}.cpp_ptr = &(({{this.type_info.lib.name.base}})(*{{param.value_name.lib}}));
{%   else %}
{{this.value_name.edk}}.cpp_ptr = reinterpret_cast< {{this.type_info.lib.name.base}} >({{param.value_name.lib}});
{%   endif %}
{% endif %}
