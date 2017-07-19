#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('OverLoadsDifferingTypes.hpp')

ext_MyClass = ext.add_managed_type('MyClass')
ext_MyClass.add_ctor(['const char *'])

ext_MyClass.add_const_method('caption', 'const char *', [])
ext_MyClass.add_mutable_method('setCaption', 'void', ['const char *'])

ext_MyClass.add_method('cast', 'const MyClass *', [Param('', 'const MyClass *')], this_access=ThisAccess.static)
ext_MyClass.add_method('cast', 'MyClass *', [Param('', 'MyClass *')], this_access=ThisAccess.static)

ext.add_test("""
  MyClass a("yay");
  report(a.caption());
  MyClass b = MyClass_cast(a);
  report(a.caption());
  a.cxx_delete();
""", """
yay
yay
""")
