#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('Opaque.hpp')

ty = ext.add_opaque_type('MyOpaque')
ty = ext.add_opaque_type('MyOpaqueDer', extends='MyOpaque')

ext.add_func('MyOpaque_New', 'MyOpaque *', ['int'])
ext.add_func('MyOpaque_New_Alt', None, ['int', 'MyOpaque **'])
ext.add_func('MyOpaque_GetX', 'int', ['MyOpaque *'])
ext.add_func('MyOpaque_SetX', None, ['MyOpaque *', 'int'])
ext.add_func('MyOpaque_Delete', None, ['MyOpaque *'])
ext.add_func('MyOpaqueDer_New', 'MyOpaqueDer *', ['int', 'float'])
ext.add_func('MyOpaqueDer_GetY', 'float', ['MyOpaqueDer *'])
ext.add_func('MyOpaqueDer_SetY', None, ['MyOpaqueDer *', 'float'])
ext.add_func('MyOpaqueDer_Delete', None, ['MyOpaqueDer *'])
ext.add_test("""
MyOpaqueDer o;
report(o);
o = MyOpaqueDer_New(17, 3.14);
report(o);
report(MyOpaque_GetX(o));
MyOpaque_SetX(o, 42);
report(MyOpaque_GetX(o));
report(MyOpaqueDer_GetY(o));
MyOpaqueDer_SetY(o, 1.24);
report(MyOpaqueDer_GetY(o));
MyOpaque oo;
report(oo);
oo = o;
report(oo);
MyOpaqueDer_Delete(o);
""", """
MyOpaqueDer:OPAQUE (null)
MyOpaqueDer:OPAQUE
17
42
+3.14
+1.24
MyOpaque:OPAQUE (null)
MyOpaque:OPAQUE
""")
ext.add_test("""
MyOpaque o;
report(o);
MyOpaque_New_Alt(17, o);
report(o);
report(MyOpaque_GetX(o));
MyOpaque_SetX(o, 42);
report(MyOpaque_GetX(o));
MyOpaque_Delete(o);
""", """
MyOpaque:OPAQUE (null)
MyOpaque:OPAQUE
17
42
""")
