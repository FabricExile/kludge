{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% extends "generate/decl/decl.defns.cpp" %}
{% block body %}
struct {{decl.type_info.const_ptr.edk.name}}
{
  {{decl.type_info.const_ptr.lib.name}} cpp_ptr;
};

struct {{decl.type_info.mutable_ptr.edk.name}}
{
  {{decl.type_info.mutable_ptr.lib.name}} cpp_ptr;
};

struct {{decl.type_info.const_ref.edk.name}}
{
  {{decl.type_info.const_ptr.lib.name}} cpp_ptr;
};

struct {{decl.type_info.mutable_ref.edk.name}}
{
  {{decl.type_info.mutable_ptr.lib.name}} cpp_ptr;
};

{% endblock body %}
