{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
if({{this.value_name.edk}}.cpp_ptr != NULL)
  delete({{this.value_name.edk}}.cpp_ptr);
