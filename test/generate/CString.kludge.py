#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('CString.hpp')

ext.add_func('CStringParams', 'const char *', ['char const *', 'char const * const &'])\
  .add_test("""
report("CxxCStringParams('value', 'constRef') = " + CxxCStringParams('value', Make_CxxCharConstPtrConstRef('constRef')));
report("CStringParams('value', 'constRef') = " + CStringParams('value', 'constRef'));
""", """
CxxCStringParams('value', 'constRef') = valueconstRef
CStringParams('value', 'constRef') = valueconstRef
""")

ext.add_func('CStringValueReturn', 'char const *')\
  .add_test("""
report("CxxCStringValueReturn() = " + CxxCStringValueReturn());
report("CStringValueReturn() = " + CStringValueReturn());
""", """
CxxCStringValueReturn() = value
CStringValueReturn() = value
""")

ext.add_func('CStringConstRefReturn', 'char const * const &')\
  .add_test("""
report("CxxCStringConstRefReturn() = " + CxxCStringConstRefReturn());
report("CStringConstRefReturn() = " + CStringConstRefReturn());
""", """
CxxCStringConstRefReturn() = constRef
CStringConstRefReturn() = constRef
""")
