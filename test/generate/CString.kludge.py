#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('CString.hpp')

ext.add_func('CStringParams')\
  .returns('const char *')\
  .add_param('char const *')\
  .add_param('char const * const &')\
  .add_test("""
report("CStringParams('value', 'constRef') = " + CStringParams('value', 'constRef'));
""", """
CStringParams('value', 'constRef') = valueconstRef
""")

ext.add_func('CStringValueReturn')\
  .returns('char const *')\
  .add_test("""
report("CStringValueReturn() = " + CStringValueReturn());
""", """
CStringValueReturn() = value
""")

ext.add_func('CStringConstRefReturn')\
  .returns('char const * const &')\
  .add_test("""
report("CStringConstRefReturn() = " + CStringConstRefReturn());
""", """
CStringConstRefReturn() = constRef
""")
