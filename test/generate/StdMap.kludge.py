#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('StdMap.hpp')

ext.add_func('ReturnValueForKey', 'float', ['std::map<float, float> const &', 'float'])\
  .add_test("""
Float32 a[Float32];
a[5.34] = 9.12;
a[-9.32] = 1.34;
report("a = " + a);
report("ReturnValueForKey(a, -9.32) = " + ReturnValueForKey(a, -9.32));
""", """
a = {+5.34:+9.12,-9.32:+1.34}
ReturnValueForKey(a, -9.32) = +1.34
""")

ext.add_func('ReturnValueForKeyKey', 'char const *', [
  'std::map< unsigned, std::map<std::string, char const *> > const &',
  'unsigned',
  'std::string const &',
  ])\
  .add_test("""
String b[UInt32][String];
b[57]["foo"] = "foo val";
b[93]["bar"] = "bar val";
b[93]["baz"] = "baz val";
report("b = " + b);
report("ReturnValueForKeyKey(b, 93, 'bar') = " + ReturnValueForKeyKey(b, 93, 'bar'));
""", """
b = {57:{"foo":"foo val"},93:{"bar":"bar val","baz":"baz val"}}
ReturnValueForKeyKey(b, 93, 'bar') = bar val
""")

ext.add_func('ReturnNestedMap', 'std::map< char const *, std::map<float, std::string> >')\
  .add_test("""
report("ReturnNestedMap() = " + ReturnNestedMap());
""", """
ReturnNestedMap() = {"foo":{-6.54:"asdf",+2.31:"qowe"},"bar":{-2.31:"asdvi",+1.56:"vibawe"}}
""")
