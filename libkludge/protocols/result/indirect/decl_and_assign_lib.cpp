{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}

{% if result.type_info.lib.var_as_pointer or result.is_pointer %}
{{result.type_info.lib.name.base}} *{{result.value_name.lib}}{{result.type_info.lib.name.suffix}} = 
{% elif result.is_mutable_reference %}
{{result.type_info.lib.name.base}} &{{result.value_name.lib}}{{result.type_info.lib.name.suffix}} = {{result.deref_pointer_prefix}}
{% else %}
{{result.type_info.lib.name.base}} {{result.value_name.lib}}{{result.type_info.lib.name.suffix}} = {{result.deref_pointer_prefix}}
{% endif %}
