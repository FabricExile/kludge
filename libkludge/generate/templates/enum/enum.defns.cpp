{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% import "generate/macros.cpp" as macros %}
{% extends "generate/decl/decl.defns.cpp" %}
{% block body %}
typedef Fabric::EDK::KL::SInt32 {{enum.type_info.edk.name}};

{% endblock body %}
