{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
if ( {{this.value_name.edk}}.is_owned )
{
  delete static_cast< ::{{this.type_info.lib.name.base}} * >( {{this.value_name.edk}}.cpp_ptr );
  {{this.value_name.edk}}.cpp_ptr = NULL;
  {{this.value_name.edk}}.is_owned = false;
}
