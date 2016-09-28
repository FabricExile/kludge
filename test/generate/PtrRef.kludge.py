#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('PtrRef.hpp')

ext.add_func('GetIntCPtrCPtrCPtr', 'int const * const * const *')\
  .add_test("""
SInt32_CxxConstPtr_CxxConstPtr_CxxConstPtr result = GetIntCPtrCPtrCPtr();
report(result.cxxDeref().cxxGet().cxxDeref().cxxGet().cxxDeref());
""", """
42
""")

ty = ext.add_owned_type('Class')
ty.add_cast('char const *', ThisAccess.const)
ty.add_test("""
Class class;
report(CxxCharConstPtr(class));
""", """
hello
""")
ty.add_method('func', None, ['void **'])
