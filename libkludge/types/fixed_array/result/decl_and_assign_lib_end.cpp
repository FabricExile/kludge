{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
;
{{result.type_info.lib.name.base}} {{result.value_name.lib}}{{result.type_info.lib.name.suffix}};
for ( size_t __i = 0; __i < {{result.conv.type_info.lib.expr.size}}; ++__i )
{
    {{result.conv.child[0].type_info.lib.name.base}} const (&{{result.conv.child[0].value_name.lib}}){{result.conv.child[0].type_info.lib.name.suffix}} = {{result.value_name.lib}}__ref[__i];
    {{result.conv.child[0].render_assign_lib(result.value_name.lib+"[__i]", result.conv.child[0].value_name.lib, "__ii") | indent(4)}}
}
