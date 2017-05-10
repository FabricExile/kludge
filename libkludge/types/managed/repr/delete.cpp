{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
if({{this.value_name.edk}}.cpp_ptr != NULL)
{
  delete(reinterpret_cast< ::{{this.type_info.lib.name.base}} >({{this.value_name.edk}}.cpp_ptr));
  {{this.value_name.edk}}.cpp_ptr = NULL;
}
