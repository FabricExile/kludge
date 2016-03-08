{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}
// {{conv.value_name.edk}}.clear();
for ( {{conv.type_info.lib.name}}::const_iterator it = {{conv.value_name.lib}}.begin();
  it != {{conv.value_name.lib}}.end(); ++it )
{
    {{conv.child[0].type_info.lib.name}} const &{{conv.child[0].value_name.lib}} = {{conv.child[0].undo_pointer_prefix}}it->first;
    {{conv.child[0].render_lib_to_edk_decl() | indent(4)}}
    {{conv.child[1].type_info.lib.name}} const &{{conv.child[1].value_name.lib}} = {{conv.child[1].undo_pointer_prefix}}it->second;
    {{conv.child[1].render_lib_to_edk_decl() | indent(4)}}
    {{conv.value_name.edk}}[{{conv.child[0].value_name.edk}}] = {{conv.child[1].value_name.edk}};
}
