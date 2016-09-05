{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}

{{conv.value_name.lib}}.clear();
{{conv.value_name.lib}}.reserve( {{conv.value_name.edk}}.size() );
for ( uint32_t i = 0; i < {{conv.value_name.edk}}.size(); ++i )
{
    {{conv.child[0].type_info.edk.name}} const &{{conv.child[0].value_name.edk}} = {{conv.value_name.edk}}[i];
    {{conv.child[0].render_edk_to_lib_decl() | indent(4)}}
    {{conv.value_name.lib}}.push_back( {{conv.child[0].value_name.lib}} );
}
