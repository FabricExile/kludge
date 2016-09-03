#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('Namespaces.hpp')

ext.add_func('GlobalFunc', 'char const *')
ns = ext.add_namespace('NameSpace')
cl = ns.add_direct_type('Class')
scl = cl.add_in_place_type('SubClass')
scl.add_member('x', 'int')
scl.add_ctor(['int'])
cl.add_ctor(['int'])
cl.add_const_method('getSubClass', 'SubClass const &')
ns.add_func('GlobalFunc', 'char const *')
nns = ns.add_namespace('NestedNameSpace')
nns.add_func('GlobalFunc', 'char const *')
