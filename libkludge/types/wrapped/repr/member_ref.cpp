{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% if this.is_mutable %}
((*{{this.value_name.edk}}.cpp_ptr)->{{cpp_member_name}})
{% else %}
(const_cast<{{this.type_info.lib.name.compound}} const &>(*{{this.value_name.edk}}.cpp_ptr)->{{cpp_member_name}})
{% endif %}
