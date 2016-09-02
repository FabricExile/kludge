{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% if this.is_mutable %}
static_cast<{{this.type_info.lib.expr.components[0].params[0]}} *>(
  {{this.value_name.edk}}.cpp_ptr->operator->()
  )->{{cpp_member_name}}
{% else %}
static_cast<{{this.type_info.lib.expr.components[0].params[0]}} const *>(
  const_cast<{{this.type_info.lib.name.compound}} const *>(
    {{this.value_name.edk}}.cpp_ptr
    )->operator->()
  )->{{cpp_member_name}}
{% endif %}
