#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('PtrRef.hpp')

ext.add_func('GetIntCPtrCPtrCPtr', 'int const * const * const *')\
  .add_test("""
CxxSInt32ConstPtrConstPtrConstPtr result = CxxGetIntCPtrCPtrCPtr();
report(result.cxx_deref().cxx_get().cxx_deref().cxx_get().cxx_deref());
report(GetIntCPtrCPtrCPtr());
""", """
42
42
""")

ty = ext.add_owned_type('Class')
ty.add_ctor([])
ty.add_cast('char const *', ThisAccess.const)
ty.add_test("""
Class class;
report(CxxCharConstPtr(class));
""", """
hello
""")
ty.add_method('func', None, ['void **'])
