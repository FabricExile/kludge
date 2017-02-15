{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
for ( size_t {{ind_name}} = 0; {{ind_name}} < {{conv.type_info.lib.expr.size}}; ++{{ind_name}} )
{
    {{conv.child[0].type_info.lib.name.base}} const (&{{conv.child[0].value_name.lib}}){{conv.child[0].type_info.lib.name.suffix}} = {{conv.child[0].deref_pointer_prefix}}{{conv.value_name.lib}}[{{ind_name}}];
    {{conv.child[0].render_lib_to_edk_decl() | indent(4)}}
    {{conv.child[0].render_assign_edk(conv.value_name.edk+"["+ind_name+"]", conv.child[0].value_name.edk, ind_name+"i") | indent(4)}}
}
