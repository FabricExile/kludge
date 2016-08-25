# ext.set_prefix('KludgeTest_')
ext.add_cpp_quoted_include('hello.h')
ext.add_func(
  'hello'
).returns(
  'std::vector<std::string>'
).add_param(
  'int'
).add_test("""
report("Result is: " + {{func.name_kl}}(4));
""", """
Called {{func.name_kl}}(4)
Result is ["foo0", "foo1", "foo2", "foo3"]
""")
