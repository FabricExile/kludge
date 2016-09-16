#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('Mirror.hpp')

ext.add_kl_prolog("""
struct KLVec2 {
  Float32 x, y;
};
""")

ext.add_mirror('CxxVec2', 'KLVec2')
ext.add_func('ReturnCxxVec2', 'CxxVec2')\
  .add_test("""
report(ReturnCxxVec2());
""", """
{x:-6.7,y:+4.2}
""")
ext.add_func('ReturnCxxVec2ConstRef', 'CxxVec2 const &')\
  .add_test("""
report(ReturnCxxVec2ConstRef());
""", """
{x:+1.2,y:-6.0}
""")
