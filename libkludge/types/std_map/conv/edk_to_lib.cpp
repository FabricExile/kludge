{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}

{{conv.value_name.lib}}.clear();
for ( {{conv.type_info.edk.name}}::CIT it = {{conv.value_name.edk}}.begin();
  it != {{conv.value_name.edk}}.end(); ++it )
{
    {{conv.child[0].type_info.edk.name}} const &{{conv.child[0].value_name.edk}} = it.key();
    {{conv.child[0].render_edk_to_lib_decl() | indent(4)}}
    {{conv.child[1].type_info.edk.name}} const &{{conv.child[1].value_name.edk}} = it.value();
    {{conv.child[1].render_edk_to_lib_decl() | indent(4)}}
    {{conv.value_name.lib}}[{{conv.child[0].value_name.lib}}] = {{conv.child[1].value_name.lib}};
}
