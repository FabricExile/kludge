#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('StdVector.hpp')

ext.add_func('ReturnSecond', 'float', ['std::vector<float>'])\
  .add_test("""
Float32 a[];
a.push(3.14);
a.push(5.34);
report("a = " + a);
report("ReturnSecond(a) = " + ReturnSecond(a));
""", """
a = [+3.14,+5.34]
ReturnSecond(a) = +5.34
""")

ext.add_func('ReturnSecondSecond', 'char const *', ['std::vector< std::vector<char const *> > const &'])\
  .add_test("""
String b[][];
b.resize(2);
b[0].resize(2);
b[0][0] = "foo";
b[0][1] = "bar";
b[1].resize(2);
b[1][0] = "baz";
b[1][1] = "buzzy";
report("b = " + b);
report("ReturnSecondSecond(b) = " + ReturnSecondSecond(b));
""", """
b = [["foo","bar"],["baz","buzzy"]]
ReturnSecondSecond(b) = buzzy
""")

ext.add_func('ReturnStringArrayArray', 'std::vector< std::vector<std::string> >')\
  .add_test("""
report("ReturnStringArrayArray() = " + ReturnStringArrayArray());
""", """
ReturnStringArrayArray() = [["hello","there","my","friend"],["hello","there","my","friend"],["hello","there","my","friend"]]
""")

ext.add_alias('StringVector', 'std::vector< std::string >')

ext.add_func('GetStringVector', 'StringVector')\
  .add_test("""
report("GetStringVector() = " + GetStringVector());
""", """
GetStringVector() = ["hello","world"]
""")

ext.add_func('AppendToStringVector', None, ['std::vector<std::string> &'])\
  .add_test("""
String s[];
s.push("before append");
AppendToStringVector(s);
report(s);
""", """
["before append","appended string"]
""")
  
