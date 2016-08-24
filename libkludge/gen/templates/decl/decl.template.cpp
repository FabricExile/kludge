{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}

//////////////////////////////////////////////////////////////////////////////
//
// KLUDGE EDK
// Description: {{ decl.desc }}
{% if decl.location %}
// C++ Source Location: {{ decl.location }}
{% endif %}
//
//////////////////////////////////////////////////////////////////////////////
//

{% for cpp_local_include in decl.cpp_local_includes %}
#include <{{cpp_local_include}}>
{% endfor %}

{% block body %}
{% endblock body %}

//
//////////////////////////////////////////////////////////////////////////////
