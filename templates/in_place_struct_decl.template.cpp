{% extends "decl.template.cpp" %}
{% block body %}
typedef ::{{ decl.name }} {{ decl.name }};
{% endblock body %}
