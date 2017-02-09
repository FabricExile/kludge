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
ty.add_mutable_method('someMethod', 'void', ['char const *'])
ty.add_mutable_method('someMethod', 'void', ['std::string const &'])
ty.add_test("""
MyType mt('onetwothreefour');
mt.someMethod("foo");
""", """
MyType::someMethod(const char *)
""")

ext.add_func("GetStaticMyType", "MyType const &")
ext.add_test("""
report("GetStaticMyType().get() = " + GetStaticMyType().get());
""", """
MyType::get()
GetStaticMyType().get() = staticMyType
""")

ext.add_func("GlobalFuncWithPromotionClash", "void", ["char const *"])
ext.add_func("GlobalFuncWithPromotionClash", "void", ["std::string const &"])
ext.add_test("""
GlobalFuncWithPromotionClash('foo');
""", """
GlobalFuncWithPromotionClash(char const *)
""")

ext.add_func("SetStdStringByRef", "void", ["std::string &"])
ext.add_func("SetStdStringByPtr", "void", ["std::string *"])
ext.add_test("""
String str;
SetStdStringByRef(str);
report("After SetStdStringByRef(str): str=" + str);
SetStdStringByPtr(str);
report("After SetStdStringByPtr(str): str=" + str);
""", """
After SetStdStringByRef(str): str=fooByRef
After SetStdStringByPtr(str): str=fooByPtr
""")
