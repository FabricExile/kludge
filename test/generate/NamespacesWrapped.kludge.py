#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('Namespaces.hpp')

ext.add_func('GlobalFunc', 'char const *')
ns = ext.add_namespace('NameSpace')
cl = ns.add_wrapped_type('Wrapper', 'Class')
scl = cl.add_in_place_type('SubClass')
scl.add_member('x', 'int')
scl.add_ctor(['int'])
cl.add_ctor(['int'])
cl.add_const_method('getSubClass', 'SubClass const &')
cl.add_enum('Enum', ['Foo', 'Bar'])
cl.add_static_method('DescEnum', 'char const *', ['Enum'])\
  .add_test("""
report(NameSpace_Class_DescEnum(NameSpace_Class_Foo));
""", """
Foo
""")
ns.add_func('GlobalFunc', 'char const *')
nns = ns.add_namespace('NestedNameSpace')
nns.add_func('GlobalFunc', 'char const *')
