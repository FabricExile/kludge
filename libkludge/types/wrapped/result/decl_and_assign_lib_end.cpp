{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
;
if ( !__wrapped_result.operator!() )
  {{result.value_name.edk}}.cpp_ptr =
    new {{result.base_type_info.lib.name.base}}( __wrapped_result );
else
  {{result.value_name.edk}}.cpp_ptr = NULL;
