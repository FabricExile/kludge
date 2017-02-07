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
CxxDescribeGlobalEnum(ValueOne);
DescribeGlobalEnum(ValueOne);
DescribeGlobalEnum(ValueSeventeen);
CxxDescribeGlobalEnum(CxxReturnGlobalEnum());
DescribeGlobalEnum(ReturnGlobalEnum());
GlobalEnum e;
CxxSetGlobalEnum(Make_CxxGlobalEnumRef(e));
CxxDescribeGlobalEnum(e);
SetGlobalEnum(e);
DescribeGlobalEnum(e);
""", """
DescribeGlobalEnum: e=ValueOne
DescribeGlobalEnum: e=ValueOne
DescribeGlobalEnum: e=ValueSeventeen
DescribeGlobalEnum: e=ValueTwo
DescribeGlobalEnum: e=ValueTwo
DescribeGlobalEnum: e=ValueTwo
DescribeGlobalEnum: e=ValueTwo
""")
ty = ext.add_enum('', ['AnonValueOne', 'AnonValueTwo'])
ty.add_test("""
report(AnonValueTwo);
""", """
1
""")
