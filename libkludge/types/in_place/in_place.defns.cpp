{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% extends "generate/decl/decl.impls.cpp" %}
{% block body %}
struct Fabric_EDK_KL_{{decl.kl_type_name}}ConstPtr
{
  {{decl.cpp_type_expr}} const *cpp_ptr;
};

struct Fabric_EDK_KL_{{decl.kl_type_name}}MutablePtr
{
  {{decl.cpp_type_expr}} *cpp_ptr;
};

struct Fabric_EDK_KL_{{decl.kl_type_name}}ConstRef
{
  {{decl.cpp_type_expr}} const *cpp_ptr;
  {{decl.cpp_type_expr}} value;
  bool is_local;
};

struct Fabric_EDK_KL_{{decl.kl_type_name}}MutableRef
{
  {{decl.cpp_type_expr}} *cpp_ptr;
  {{decl.cpp_type_expr}} value;
  bool is_local;
};

{% endblock body %}
