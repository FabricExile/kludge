{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
if ( &{{conv.value_name.lib}} != {{conv.value_name.edk}}.cpp_ptr )
{
  delete static_cast< ::{{conv.type_info.lib.name.base}} * >( {{conv.value_name.edk}}.cpp_ptr );
  {{conv.value_name.edk}}.cpp_ptr = new {{conv.type_info.lib.name.compound}}( {{conv.value_name.lib}} );
}
