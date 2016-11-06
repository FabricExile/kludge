#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('FuncWithOptionalParams.hpp')
ext.add_func(
  'FuncWithOptionalParams',
  None,
  ['int'],
  ['float'],
).add_test("""
FuncWithOptionalParams(56);
FuncWithOptionalParams(-7, 5.12);
""", """
FuncWithOptionalParams a=56 b=4.65
FuncWithOptionalParams a=-7 b=5.12
""")
