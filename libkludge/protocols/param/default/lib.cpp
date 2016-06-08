{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}

{% if param.type_info.lib.var_as_pointer %}
{{param.value_name.lib}}
{% else %}
{{param.take_pointer_prefix}}{{param.value_name.lib}}
{% endif %}
