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
report("CxxReturnAliasValue() = " + CxxReturnAliasValue());
report("ReturnAliasValue() = " + ReturnAliasValue());
""", """
CxxReturnAliasValue() = 63
ReturnAliasValue() = 63
""")

ext.add_func('TakeAliasType', None, ['AliasType'])\
  .add_test("""
AliasType cxx_alias_value = 42;
CxxTakeAliasType(cxx_alias_value);
AliasType alias_value = 42;
TakeAliasType(alias_value);
report("<empty>");
""", """
<empty>
""")

ext.add_func('TakeAliasTypeRef', None, ['AliasType &'])\
  .add_test("""
AliasType cxx_alias_value = 42;
CxxTakeAliasTypeRef(Make_CxxAliasTypeRef(cxx_alias_value));
AliasType alias_value = 42;
TakeAliasTypeRef(alias_value);
report("<empty>");
""", """
<empty>
""")

ext.add_func('TakeAliasTypeConstRef', None, ['AliasType const &'])\
  .add_test("""
AliasType cxx_alias_value = 42;
CxxTakeAliasTypeConstRef(Make_CxxAliasTypeConstRef(cxx_alias_value));
AliasType alias_value = 42;
TakeAliasTypeConstRef(alias_value);
report("<empty>");
""", """
<empty>
""")
