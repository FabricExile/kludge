{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
if ( {{param.value_name.edk}}.cpp_ptr )
{
  {{this.value_name.edk}}.cpp_ptr = new ::{{this.type_info.lib.name.base}}(
    *static_cast< ::{{this.type_info.lib.name.base}} const * >( {{param.value_name.edk}}.cpp_ptr )
    );
  {{this.value_name.edk}}.is_owned = true;
}
else
{
  {{this.value_name.edk}}.cpp_ptr = NULL;
  {{this.value_name.edk}}.is_owned = false;
}
