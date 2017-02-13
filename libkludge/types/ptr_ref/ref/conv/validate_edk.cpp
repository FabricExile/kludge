{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
if ( !{{conv.value_name.edk}}.cpp_ptr )
  ::Fabric::EDK::throwException( "dereferenced null {{conv.type_info.lib.name}} pointer" );
