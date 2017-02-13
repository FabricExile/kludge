#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('PromotionProlog.hpp')

ty = ext.add_owned_type('Class')
ty.add_ctor()
ty.add_mutable_method(
  'publicMethod', None,
  [Param('str', 'std::string const &')],
  promotion_prolog="""
if (!str)
  throw 'Must call with non-empty string';
""")
ty.add_test("""
Class c;
c.publicMethod('');
""", """
Error: Must call with non-empty string
KL stack trace:
""", skip_epilog=True)
