#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('Aliases.hpp')

ext.add_alias('AliasType', 'unsigned')\
  .add_test("""
AliasType alias_value = 42;
report(alias_value.type());
report(alias_value);
""", """
UInt32
42
""")

ext.add_func('ReturnAliasValue', 'AliasType')\
  .add_test("""
report("ReturnAliasValue() = " + ReturnAliasValue());
""", """
ReturnAliasValue() = 63
""")

ext.add_func('TakeAliasType', None, ['AliasType'])\
  .add_test("""
AliasType alias_value = 42;
TakeAliasType(alias_value);
report("<empty>");
""", """
<empty>
""")

ext.add_func('TakeAliasTypeRef', None, ['AliasType &'])\
  .add_test("""
AliasType alias_value = 42;
TakeAliasTypeRef(Make_AliasType_CxxRef(alias_value));
report("<empty>");
""", """
<empty>
""")

ext.add_func('TakeAliasTypeConstRef', None, ['AliasType const &'])\
  .add_test("""
AliasType alias_value = 42;
TakeAliasTypeConstRef(Make_AliasType_CxxConstRef(alias_value));
report("<empty>");
""", """
<empty>
""")
