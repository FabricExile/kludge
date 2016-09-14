{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% extends "generate/decl/decl.fwds.cpp" %}
{% block body %}
{% if not decl.is_simple %}
typedef {{decl.type_info.lib.name}} {{decl.type_info.edk.name}};
{% endif %}

{% endblock body %}
