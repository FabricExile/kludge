{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
struct {{this.type_info.edk.name}}
{% if this.extends_this %}
  : public {{this.extends_this.type_info.edk.name}}
  {};
{% else %}
{
  ::{{this.type_info.lib.name.base}} *cpp_ptr{{this.type_info.lib.name.suffix}};
};
{% endif %}
