{% extends "decl.template.cpp" %}
{% block body %}
namespace Fabric { namespace EDK { namespace KL {

typedef {{ decl.type.cpp.name }} {{ decl.type.edk.local_name }};

} } }
{% endblock body %}
