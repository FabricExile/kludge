{% extends "decl.template.cpp" %}
{% block body %}
typedef ::{{ decl.type_name }} {{ decl.type_name }};
{% endblock body %}
