{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
for ( size_t {{ind_name}} = 0; {{ind_name}} < {{conv.type_info.lib.expr.size}}; ++{{ind_name}} )
{
    {{conv.child[0].type_info.edk.name}} const (&{{conv.child[0].value_name.edk}}) = {{conv.value_name.edk}}[{{ind_name}}];
    {{conv.child[0].render_edk_to_lib_decl() | indent(4)}}
    {{conv.child[0].render_assign_lib(conv.value_name.lib+"["+ind_name+"]", conv.child[0].value_name.lib, ind_name+"i") | indent(4)}}
}
