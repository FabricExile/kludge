# ext.set_prefix('KludgeTest_')
ext.add_cpp_quoted_include('hello.hpp')
ext.add_func(
  'hello'
).add_test("""
hello();
""", """
Hello, world!
""")
