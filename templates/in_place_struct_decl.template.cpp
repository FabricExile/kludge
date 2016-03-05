{% extends "decl.template.cpp" %}
{% block body %}
typedef {{ decl.type.cpp.name }} {{ decl.type.edk.local_name }};
{% endblock body %}
