#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('FixedArray.hpp')

ty = ext.add_in_place_type('MyXfo')
ty.add_member('pos', 'float[3]')
ty.add_member('ori', 'float[4]')
ty.add_member('scaleShear', 'float[3][3]')
ty.add_ctor()
ty.add_test("""
MyXfo xfo;
report(xfo);
""", """
""")
