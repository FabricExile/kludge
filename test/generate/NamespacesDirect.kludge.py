#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('Namespaces.hpp')

ext.add_func('GlobalFunc', 'char const *')
ns = ext.add_namespace('NameSpace')
cl = ns.add_owned_type('Class')
scl = cl.add_in_place_type('SubClass')
scl.add_member('x', 'int')
scl.add_ctor(['int'])
scl.add_alias('Typedefed', 'std::string')\
  .add_test("""
NameSpace_Class_SubClass_Typedefed x = 3;
report(x);
""", """
3
""")
cl.add_ctor(['int'])
cl.add_const_method('getSubClass', 'SubClass const &')
cl.add_enum('Enum', ['Foo', 'Bar'])
cl.add_static_method('DescEnum', 'char const *', ['Enum'])\
  .add_test("""
report(NameSpace_Class_DescEnum(NameSpace_Class_Foo));
""", """
Foo
""")
cl.add_alias('Typedefed', 'SubClass')\
  .add_test("""
report(NameSpace_Class_Typedefed(42));
""", """
{x:42}
""")
ns.add_alias('Typedefed', 'Class')\
  .add_test("""
report(NameSpace_Typedefed(-7));
""", """
NameSpace_Class:{}
""")
ns.add_func('GlobalFunc', 'char const *')
nns = ns.add_namespace('NestedNameSpace')
nns.add_func('GlobalFunc', 'char const *')
