{% macro edk_param_list(result_codec, this_codec, params) %}
  {% set need_comma = False %}
  {% set indirect_param_edk = result_codec.render_indirect_param_edk() %}
  {% if indirect_param_edk %}
{{ indirect_param_edk }}
    {% set need_comma = True %}
  {% endif %}
  {% if this_codec %}
{{ ", " if need_comma else "" }}{{this_codec.render_param_edk()}}
    {% set need_comma = True %}
  {% endif %}
  {% for param in params %}
{{ "," if loop.first and need_comma else "" }}
{{ param.render_edk() }}{{ "," if not loop.last else "" }}
  {% endfor %}
{% endmacro %}

{% macro cpp_call_pre(result_codec, params) %}
{{ result_codec.render_indirect_init_edk() }}
  
  {% for param in params %}
{{ param.render_edk_to_lib_decl() }}
  {% endfor %}
  {% if result_codec %}

{{ result_codec.render_decl_and_assign_lib_begin() }}
  {% endif %}
{% endmacro %}

{% macro cpp_call_args(params) %}
  {% for param in params %}
{{param.render_lib()}}{{"," if not loop.last else ""}}
  {% endfor %}
{% endmacro %}

{% macro cpp_call_post(result_codec, params) %}
  {% if result_codec %}
{{ result_codec.render_decl_and_assign_lib_end() }}

  {% endif %}
  {% for param in params %}
{{ param.render_lib_to_edk() }}
  {% endfor %}
  
{{ result_codec.render_indirect_lib_to_edk() }}
{{ result_codec.render_direct_return_edk() }}
{% endmacro %}
