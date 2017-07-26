#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('Casts.hpp')

vecType = ext.add_mirror('MyVec', 'Vec2_d', 'Math')

classType = ext.add_managed_type('Class')
classType.add_ctor(['double', 'double'])
classType.add_const_method('x', 'double')
classType.add_const_method('y', 'double')
classType.add_cast('double *', this_access=ThisAccess.mutable)
classType.add_cast('const double *', this_access=ThisAccess.const)
classType.add_cast('MyVec &', this_access=ThisAccess.mutable)

classType.add_test("""
  Class c(2, 3);
  report(c.x());
  report(c.y());
  CxxFloat64ConstPtr ptr(c);
  report(ptr.cxx_getAt(0));
  report(ptr.cxx_getAt(1));
  CxxMyVecRef v = c;
  report(v.cxx_get());
""", """
+2.0
+3.0
+2.0
+3.0
{x:+2.0,y:+3.0}
""")
