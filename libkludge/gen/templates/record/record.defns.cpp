{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% import "gen/macros.cpp" as macros %}
{% extends "gen/decl/decl.defns.cpp" %}
{% block body %}
{{decl.mutable_this.render_defn_edk()}}

{% endblock body %}
