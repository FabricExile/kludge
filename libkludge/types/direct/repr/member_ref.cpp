{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% if this.is_mutable %}
(static_cast< ::{{this.type_info.lib.name.base}} * >({{this.value_name.edk}}.cpp_ptr)->{{cpp_member_name}})
{% else %}
(static_cast< ::{{this.type_info.lib.name.base}} const * >({{this.value_name.edk}}.cpp_ptr)->{{cpp_member_name}})
{% endif %}
