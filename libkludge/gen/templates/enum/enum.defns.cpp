{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% import "gen/macros.cpp" as macros %}
{% extends "gen/decl/decl.defns.cpp" %}
{% block body %}
typedef Fabric::EDK::KL::SInt32 {{enum.type_info.edk.name}};

{% endblock body %}
