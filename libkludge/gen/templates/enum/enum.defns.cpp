{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% import "gen/macros.cpp" as macros %}
{% extends "gen/decl/decl.defns.cpp" %}
{% block body %}
namespace Fabric { namespace EDK { namespace KL {
typedef SInt32 {{enum.type_info.edk.name.local}};
} } }

{% endblock body %}
