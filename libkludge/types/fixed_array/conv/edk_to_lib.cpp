{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}

for ( unsigned _KLUDGE_INDEX = 0; _KLUDGE_INDEX < {{conv.type_info.lib.expr.size}}; ++_KLUDGE_INDEX )
{
    {{conv.child[0].type_info.edk.name}} const &{{conv.child[0].value_name.edk}} = {{conv.value_name.edk}}[_KLUDGE_INDEX];
    {{conv.child[0].render_edk_to_lib_decl() | indent(4)}}
    {{conv.value_name.lib}}[_KLUDGE_INDEX] = {{conv.child[0].value_name.lib}};
}
