{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% extends "generate/decl/decl.impls.cpp" %}
{% block body %}
{{decl.render_method_impls('cpp')}}
FABRIC_EXT_EXPORT Fabric::EDK::KL::UInt64
__CxxSize_{{decl.type_info.edk.name}}()
{
  return sizeof({{decl.type_info.lib.name}});
}

{% endblock body %}
