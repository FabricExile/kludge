{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
{% extends "generate/decl/decl.defns.cpp" %}
{% block body %}
typedef {{decl.type_info.lib.name}} {{decl.type_info.edk.name}};

{% endblock body %}
