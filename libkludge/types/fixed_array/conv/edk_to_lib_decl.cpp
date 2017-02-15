{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
{% set r = conv.type_info.lib.expr.range %}
{% for i in r %}
{{conv.child[0].type_info.edk.name}} const &{{conv.child[0].value_name.edk}}__{{i}} = {{conv.value_name.edk}}[{{i}}];
{% endfor %}
{{conv.type_info.lib.name.base}} {{conv.value_name.lib}}{{conv.type_info.lib.name.suffix}} =
{
  {% for i in r %}
  {{conv.child[0].value_name.edk}}__{{i}}{{"," if not loop.last else ""}}
  {% endfor %}
};
