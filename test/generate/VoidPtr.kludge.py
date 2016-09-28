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
ty = ext.add_owned_type('Class')
ty.add_cast('void *', this_access=ThisAccess.mutable)
ty.add_cast('void const *', this_access=ThisAccess.const)
ty.add_test("""
Class class;
report(Data(class));
""", """
<Opaque>
""")
