{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
if ( !{{this.value_name.edk}}.cpp_ptr )
    {{this.value_name.edk}}.cpp_ptr = new ::{{this.type_info.lib.name.base}}(
        {{param.render_lib()}}
        );
else
    *{{this.value_name.edk}}.cpp_ptr =
        {{param.render_lib()}};
