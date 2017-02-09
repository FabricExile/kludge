#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('StdVector.hpp')

ext.generate_type("std::vector<int>")
ext.add_test("""
CxxSInt32StdVector vec;
report(vec.size());
vec.push_back(-7);
report(vec.size());
report(vec.cxx_getAtIndex(0));
vec.cxx_setAtIndex(0, Make_CxxSInt32ConstRef(42));
report(vec.cxx_getAtIndex(0));
vec.pop_back();
report(vec.size());
""", """
0
1
-7
42
0
""")

ext.add_func('ReturnSecond', 'float', ['std::vector<float>'])
ext.add_test("""
Float32 a[];
a.push(3.14);
a.push(5.34);
report("a = " + a);
report("CxxReturnSecond(a) = " + CxxReturnSecond(CxxFloat32StdVector(a)));
""", """
a = [+3.14,+5.34]
CxxReturnSecond(a) = +5.34
""")
ext.add_test("""
CxxFloat32StdVector a;
a.cxx_push_back(3.14);
a.cxx_push_back(5.34);
report("a = " + a);
report("CxxReturnSecond(a) = " + CxxReturnSecond(a));
""", """
a = CxxFloat32StdVector:[+3.14,+5.34]
CxxReturnSecond(a) = +5.34
""")
ext.add_test("""
Float32 a[];
a.push(3.14);
a.push(5.34);
report("a = " + a);
report("ReturnSecond(a) = " + ReturnSecond(a));
""", """
a = [+3.14,+5.34]
ReturnSecond(a) = +5.34
""")

ext.add_func('ReturnIntVec', 'std::vector<int>')\
  .add_test("""
report(Make_SInt32VariableArray(ReturnIntVec()));
""", """
[-7,42]
""")

ext.add_func('GlobalTakingStdVectorConstRef', None, ['std::vector<int> const &'])\

ext.add_func('SetStdVectorFromRef', None, ['std::vector<int> &'])
ext.add_test("""
SInt32 v[];
SetStdVectorFromRef(v);
report(v);
""", """
[56,-7,1983]
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
  
