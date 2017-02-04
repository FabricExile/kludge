{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
{% import "generate/macros.cpp" as macros %}
{% extends "generate/decl/decl.defns.cpp" %}
{% block body %}
{% if enum.type_info %}
typedef Fabric::EDK::KL::SInt32 {{enum.type_info.edk.name}};

{% endif %}
{% endblock body %}
