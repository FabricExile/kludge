{######################################################################}
{# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved. #}
{######################################################################}

{{conv.value_name.edk}}.resize( 0 );
for ( {{conv.type_info.lib.name}}::const_iterator it = {{conv.value_name.lib}}.begin();
  it != {{conv.value_name.lib}}.end(); ++it )
{
    {{conv.child[0].type_info.lib.name}} const &{{conv.child[0].value_name.lib}} = {{conv.child[0].deref_pointer_prefix}}*it;
    {{conv.child[0].render_lib_to_edk_decl() | indent(4)}}
    {{conv.value_name.edk}}.push( {{conv.child[0].value_name.edk}} );
}
