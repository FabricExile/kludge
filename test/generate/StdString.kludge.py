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

ty = ext.add_owned_type("MyType")
ty.add_ctor(["std::string const &"])
ty.add_const_method("get", "std::string const &")
ty.add_test("""
report("MyType('onetwothreefour').get() = " + MyType('onetwothreefour').get());
""", """
MyType::get()
MyType('onetwothreefour').get() = onetwothreefour
""")

ext.add_func("GetStaticMyType", "MyType const &")\
  .add_test("""
report("GetStaticMyType().get() = " + GetStaticMyType().get());
""", """
MyType::get()
GetStaticMyType().get() = staticMyType
""")
