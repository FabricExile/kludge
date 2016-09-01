{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
struct {{this.type_info.edk.name.local}}
{% if this.extends_this %}
  : {{this.extends_this.type_info.edk.name.local}}
  {};
{% else %}
{
  ::{{this.type_info.lib.name.base}} *cpp_ptr{{this.type_info.lib.name.suffix}};
  bool is_owned;
};
{% endif %}
