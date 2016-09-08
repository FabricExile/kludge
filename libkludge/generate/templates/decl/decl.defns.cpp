{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
//////////////////////////////////////////////////////////////////////////////
//
// {{ decl.desc }} - Definitions
//
//////////////////////////////////////////////////////////////////////////////
{% if decl.cpp_local_includes %}

{% for cpp_local_include in decl.cpp_local_includes %}
#include <{{cpp_local_include}}>
{% endfor %}
{% endif %}

{% block body %}
{% endblock body %}
