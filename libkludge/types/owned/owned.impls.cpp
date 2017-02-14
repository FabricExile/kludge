{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
{% extends "generate/decl/decl.impls.cpp" %}
{% block body %}
{{decl.render_method_impls('cpp')}}
FABRIC_EXT_EXPORT Fabric::EDK::KL::UInt64
{{decl.type_info.cxx_size_func_name}}()
{
  return sizeof({{decl.type_info.lib.name}});
}

{% endblock body %}
