#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('hello.hpp')
ext.add_func(
  'hello'
).add_test("""
hello();
""", """
Hello, world!
""")
