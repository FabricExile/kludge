{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% extends "generate/decl/decl.defns.cpp" %}
{% block body %}
struct {{decl.type_info.edk.name}}
{% if decl.type_info.extends %}
  : public {{decl.type_info.extends.edk.name}}
  {};
{% else %}
{
  ::{{decl.type_info.lib.name.base}} *cpp_ptr{{decl.type_info.lib.name.suffix}};
};
{% endif %}

{% endblock body %}
