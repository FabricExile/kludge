#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('Enums.hpp')

ty = ext.add_enum('GlobalEnum', [
  'ValueZero',
  'ValueOne',
  'ValueTwo',
  ('ValueSeventeen', 17),
  ])
ext.add_func('DescribeGlobalEnum', None, ['GlobalEnum'])
ext.add_func('ReturnGlobalEnum', 'GlobalEnum')
ext.add_func('SetGlobalEnum', None, ['GlobalEnum &'])
ty.add_test("""
DescribeGlobalEnum(ValueOne);
DescribeGlobalEnum(ValueSeventeen);
DescribeGlobalEnum(ReturnGlobalEnum());
GlobalEnum e;
SetGlobalEnum(Make_GlobalEnum_CxxRef(e));
DescribeGlobalEnum(e);
""", """
DescribeGlobalEnum: e=ValueOne
DescribeGlobalEnum: e=ValueSeventeen
DescribeGlobalEnum: e=ValueTwo
DescribeGlobalEnum: e=ValueTwo
""")
