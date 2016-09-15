#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('CString.hpp')

ext.add_func('CStringParams', 'const char *', ['char const *', 'char const * const &'])\
  .add_test("""
report("CStringParams('value', 'constRef') = " + CStringParams('value', Make_CxxCharConstPtrConstRef('constRef')));
""", """
CStringParams('value', 'constRef') = valueconstRef
""")

ext.add_func('CStringValueReturn', 'char const *')\
  .add_test("""
report("CStringValueReturn() = " + CStringValueReturn());
""", """
CStringValueReturn() = value
""")

ext.add_func('CStringConstRefReturn', 'char const * const &')\
  .add_test("""
report("CStringConstRefReturn() = " + CStringConstRefReturn());
""", """
CStringConstRefReturn() = constRef
""")
