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

ext.add_func('ReturnAliasValue')\
  .returns('AliasType')\
  .add_test("""
report("ReturnAliasValue() = " + ReturnAliasValue());
""", """
ReturnAliasValue() = 63
""")

ext.add_func('TakeAliasType')\
  .add_param('AliasType')\
  .add_test("""
AliasType alias_value = 42;
TakeAliasType(alias_value);
report("<empty>");
""", """
<empty>
""")

ext.add_func('TakeAliasTypeRef')\
  .add_param('AliasType &')\
  .add_test("""
AliasType alias_value = 42;
TakeAliasTypeRef(alias_value);
report("<empty>");
""", """
<empty>
""")

ext.add_func('TakeAliasTypeConstRef')\
  .add_param('AliasType const &')\
  .add_test("""
AliasType alias_value = 42;
TakeAliasTypeConstRef(alias_value);
report("<empty>");
""", """
<empty>
""")
