#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('ExceptionProlog.hpp')

ext.set_cpp_exception_prolog("""
try
{
""")
ext.set_cpp_exception_epilog("""
}
catch(std::runtime_error e)
{
  std::string message = "Caught runtime_error: ";
  message += e.what();
  Fabric::EDK::throwException(message.c_str());
}
""")

ty = ext.add_owned_type('Class')
ty.add_ctor()
ty.add_mutable_method(
  'publicMethod', None,
  [Param('str', 'std::string const &')]
  ).add_test("""
Class c;
c.publicMethod('');
""", """
Error: ExceptionProlog: Caught runtime_error: publicMethod: Empty string
KL stack trace:
""", skip_epilog=True)
