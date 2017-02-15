{############################################################################}
{# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.        #}
{############################################################################}
for (size_t {{ind_name}} = 0; {{ind_name}} < {{conv.type_info.lib.expr.size}}; ++{{ind_name}} ) {
  {{conv.child[0].render_assign_lib(lhs_name+"["+ind_name+"]", rhs_name+"["+ind_name+"]", ind_name+"i")}}
}
