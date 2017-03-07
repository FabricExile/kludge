{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
{% extends "generate/decl/decl.fwds.cpp" %}
{% block body %}
{% if decl.is_simple %}
{% if decl.type_info.kl.name.base == 'CxxChar' %}

typedef char {{decl.type_info.edk.name}};
{% endif %}
{% elif decl.is_initial_kl_type_inst %}

typedef {{decl.type_info.lib.name}} {{decl.type_info.edk.name}};
{% endif %}
{% endblock body %}
