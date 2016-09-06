{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% import "generate/macros.cpp" as macros %}
{% extends "generate/decl/decl.defns.cpp" %}
{% block body %}
{{decl.mutable_this.render_defn_edk()}}

{% endblock body %}
