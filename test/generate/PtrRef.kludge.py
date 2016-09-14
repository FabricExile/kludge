#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('PtrRef.hpp')

ext.add_func('GetIntCPtrCPtrCPtr', 'int const * const * const *')\
  .add_test("""
SInt32_CxxConstPtr_CxxConstPtr_CxxConstPtr result = GetIntCPtrCPtrCPtr();
report(result.cxxPtrDeref().cxxRefGet().cxxPtrDeref().cxxRefGet().cxxPtrDeref());
""", """
42
""")
