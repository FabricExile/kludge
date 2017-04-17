{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
{% extends "generate/decl/decl.impls.cpp" %}
{% block body %}
{{decl.render_method_impls('cpp')}}

{% endblock body %}
