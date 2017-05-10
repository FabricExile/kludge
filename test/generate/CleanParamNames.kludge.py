#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('CleanParamNames.hpp')

ty = ext.add_owned_type('Class')
ty.add_ctor([])
ty.add_member('Size', 'double')
ty.add_mutable_method('Init', None, [Param('entry', 'double')])

ty.add_test("""
Class c;
c.set_Size(12);
report(c.get_Size());

c.Init(4);
report(c.get_Size());
""", """
+12.0
+4.0
""")
