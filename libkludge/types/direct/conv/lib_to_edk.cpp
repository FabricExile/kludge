{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
if ( &{{conv.value_name.lib}} != {{conv.value_name.edk}}.cpp_ptr )
{
  if ( {{conv.value_name.edk}}.is_owned )
    delete {{conv.value_name.edk}}.cpp_ptr;
  {{conv.value_name.edk}}.cpp_ptr = new {{conv.type_info.lib.name.compound}}( {{conv.value_name.lib}} );
  {{conv.value_name.edk}}.is_owned = true;
}
