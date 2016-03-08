{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}

{% if param.is_mutable %}
{{param.conv.render_lib_to_edk()}}
{% endif %}
