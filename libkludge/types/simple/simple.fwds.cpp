{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% extends "generate/decl/decl.fwds.cpp" %}
{% block body %}
struct Fabric_EDK_KL_{{decl.kl_type_name}}ConstPtr;
struct Fabric_EDK_KL_{{decl.kl_type_name}}MutablePtr;
struct Fabric_EDK_KL_{{decl.kl_type_name}}ConstRef;
struct Fabric_EDK_KL_{{decl.kl_type_name}}MutableRef;

{% endblock body %}
