#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('StdString.hpp')

ext.add_func('ReturnStdString', 'std::string')\
  .add_test("""
report(ReturnStdString());
""", """
foo
""")

ext.add_func('ReturnStdStringConstRef', 'std::string const &')\
  .add_test("""
report(ReturnStdStringConstRef());
""", """
foo
""")
