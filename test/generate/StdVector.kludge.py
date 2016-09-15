#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('StdVector.hpp')

ext.generate_type("std::vector<int>")
ext.add_test("StdVector_basics", """
SInt32_StdVector vec;
report(vec.size());
vec.push_back(-7);
report(vec.size());
report(vec.getAt(0));
vec.setAt(0, Make_SInt32_CxxConstRef(42));
report(vec.getAt(0));
vec.pop_back();
report(vec.size());
""", """
0
1
-7
42
0
""")

ext.add_func('ReturnSecond', 'float', ['std::vector<float>'])\
  .add_test("""
Float32 a[];
a.push(3.14);
a.push(5.34);
report("a = " + a);
report("ReturnSecond(a) = " + ReturnSecond(Make_Float32_StdVector(a)));
""", """
a = [+3.14,+5.34]
ReturnSecond(a) = +5.34
""")

ext.add_func('ReturnIntVec', 'std::vector<int>')\
  .add_test("""
report(Make_SInt32_VariableArray(ReturnIntVec()));
""", """
[-7,42]
""")

# ext.add_func('ReturnStringArrayArray', 'std::vector< std::vector<std::string> >')\
#   .add_test("""
# report("ReturnStringArrayArray() = " + ReturnStringArrayArray());
# """, """
# ReturnStringArrayArray() = [["hello","there","my","friend"],["hello","there","my","friend"],["hello","there","my","friend"]]
# """)

# ext.add_alias('StringVector', 'std::vector< std::string >')

# ext.add_func('GetStringVector', 'StringVector')\
#   .add_test("""
# report("GetStringVector() = " + GetStringVector());
# """, """
# GetStringVector() = ["hello","world"]
# """)

# ext.add_func('AppendToStringVector', None, ['std::vector<std::string> &'])\
#   .add_test("""
# String s[];
# s.push("before append");
# AppendToStringVector(s);
# report(s);
# """, """
# ["before append","appended string"]
# """)
  
