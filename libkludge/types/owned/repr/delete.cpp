{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
{% if not this.type_info.dont_delete %}
delete static_cast< ::{{this.type_info.lib.name.base}} * >( {{this.value_name.edk}}.cpp_ptr );
{% endif %}
{{this.value_name.edk}}.cpp_ptr = NULL;
