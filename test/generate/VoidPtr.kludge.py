#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('VoidPtr.hpp')

ext.add_func('FunctionTakingVoidPtr', 'void *', ['void *'])\
  .add_test("""
UInt32 x = 7;
report("FunctionTakingVoidPtr(x.data()) = " + FunctionTakingVoidPtr(x.data()));
""", """
FunctionTakingVoidPtr(x.data()) = <Opaque>
""")
