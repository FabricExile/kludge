{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
for ( uint32_t _KLUDGE_INDEX = 0; _KLUDGE_INDEX < {{conv.type_info.lib.expr.size}}; ++_KLUDGE_INDEX )
{
    {{conv.child[0].type_info.lib.name.base}} const &{{conv.child[0].value_name.lib}}{{conv.child[0].type_info.lib.name.suffix}} = {{conv.child[0].deref_pointer_prefix}}{{conv.value_name.lib}}[_KLUDGE_INDEX];
    {{conv.child[0].render_lib_to_edk_decl() | indent(4)}}
    {{conv.value_name.edk}}[_KLUDGE_INDEX] = {{conv.child[0].value_name.edk}};
}
