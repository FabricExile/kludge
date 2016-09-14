{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
{% if forbid_copy %}
{{this.value_name.edk}}.cpp_ptr = {{param.value_name.edk}}.cpp_ptr;
const_cast< ::Fabric::EDK::KL::Traits< {{param.type_info.edk.name}} >::IOParam >( {{param.value_name.edk}} ).cpp_ptr = NULL;
{% else %}
if ( !{{this.value_name.edk}}.cpp_ptr )
{
  if ( {{param.value_name.edk}}.cpp_ptr )
    {{this.value_name.edk}}.cpp_ptr =
      new ::{{this.type_info.lib.name.base}}(
        *static_cast< ::{{this.type_info.lib.name.base}} const * >( {{param.value_name.edk}}.cpp_ptr )
        );
}
else
{
  if ( {{param.value_name.edk}}.cpp_ptr )
  {
    *static_cast< ::{{this.type_info.lib.name.base}} * >( {{this.value_name.edk}}.cpp_ptr ) =
      *static_cast< ::{{this.type_info.lib.name.base}} const * >( {{param.value_name.edk}}.cpp_ptr );
  }
  else
  {
    delete static_cast< ::{{this.type_info.lib.name.base}} * >( {{this.value_name.edk}}.cpp_ptr );
    {{this.value_name.edk}}.cpp_ptr = NULL;
  }
}
{% endif %}
