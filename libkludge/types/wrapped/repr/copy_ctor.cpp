{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
if ( {{param.value_name.edk}}.cpp_ptr ) {
  if ( !{{param.value_name.edk}}.cpp_ptr->operator!() )
    {{this.value_name.edk}}.cpp_ptr =
      new ::{{this.base_type_info.lib.name.base}}(
        static_cast< ::{{this.type_info.lib.expr.components[0].params[0]}} * >(
          {{param.value_name.edk}}.cpp_ptr->operator->()
          )
        );
  else
    {{this.value_name.edk}}.cpp_ptr = NULL;
}
else
  {{this.value_name.edk}}.cpp_ptr = NULL;
