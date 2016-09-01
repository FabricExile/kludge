{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
if ( !{{this.value_name.edk}}.cpp_ptr )
{
  if ( {{param.value_name.edk}}.cpp_ptr )
    {{this.value_name.edk}}.cpp_ptr =
      new ::{{this.type_info.lib.name.base}}(
        *{{param.value_name.edk}}.cpp_ptr
        );
}
else
{
  if ( {{param.value_name.edk}}.cpp_ptr )
    *{{this.value_name.edk}}.cpp_ptr =
        *{{param.value_name.edk}}.cpp_ptr;
  else
  {
    delete {{this.value_name.edk}}.cpp_ptr;
    {{this.value_name.edk}}.cpp_ptr = NULL;
  }
}
