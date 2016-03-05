{% macro edk_result_type(result_codec) %}
  {% if result_codec %}
{{ result_codec.result_direct_type_edk() }}
  {% else %}
void
  {% endif %}
{% endmacro %}

{% macro edk_param_list(result_codec, self_codec, param_codecs) %}
  {% set need_comma = False %}
  {% if result_codec %}
    {% set indirect_param_edk = result_codec.result_indirect_param_edk() %}
    {% if indirect_param_edk %}
{{ indirect_param_edk }}
      {% set need_comma = True %}
    {% endif %}
  {% endif %}
  {% if self_codec %}
{{ ", " if need_comma else "" }}{{ self_codec.param_edk() }}
    {% set need_comma = True %}
  {% endif %}
  {% for param_codecs in param_codecs %}
{{ ", " if need_comma else "" }}{{ param_codecs.param_edk() }}
    {% set need_comma = True %}
  {% endfor %}
{% endmacro %}

{% macro cpp_call_pre(result_codec, param_codecs) %}
  {% if result_codec %}
{{ result_codec.result_indirect_init_edk() }}
  
  {% endif %}
  {% for param_codec in param_codecs %}
{{ param_codec.param_edk_to_cpp_decl() }}
  {% endfor %}
  {% if result_codec %}

{{ result_codec.result_decl_and_assign_cpp() }}
  {% endif %}
{% endmacro %}

{% macro cpp_call_args(param_codecs) %}
  {% for param_codec in param_codecs %}
{{ param_codec.param_cpp() }}{{ "," if not loop.last else "" }}
  {% endfor %}
{% endmacro %}

{% macro cpp_call_post(result_codec, param_codecs) %}
  {% for param_codec in param_codecs %}
{{ param_codec.param_cpp_to_edk() }}
  {% endfor %}
  {% if result_codec %}
    {{ result_codec.result_indirect_assign_to_edk() }}
    {{ result_codec.result_direct_return_edk() }}
  {% endif %}
{% endmacro %}
