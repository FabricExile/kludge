{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% import "gen/macros.cpp" as macros %}
{% extends "gen/decl/decl.defns.cpp" %}
{% block body %}
namespace Fabric { namespace EDK { namespace KL {

struct {{decl.this_type_info.edk.name.local}} {
  ::{{decl.this_type_info.lib.name.base}} *cpp_ptr{{decl.this_type_info.lib.name.suffix}};
};

} } }
{% endblock body %}
