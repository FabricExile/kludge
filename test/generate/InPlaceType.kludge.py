#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('InPlaceType.hpp')

ty = ext.add_in_place_type('Class')
ty.add_ctor()
ty.add_ctor(['int', 'float']).add_test("""
Class c(-7, 1.52);
report("c.intValue = " + c.intValue);
report("c.GET_intValue() = " + c.GET_intValue());
""", """
Class::Class(-7, 1.52)
c.intValue = -7
c.GET_intValue() = -7
Class::~Class()
""")
ty.add_test("""
Class c1(6, 1.3);
Class c2(c1);
c1 = c2;
""", """
Class::Class(6, 1.3)
Class::Class(Class const &)
Class::operator=(Class const &)
Class::~Class()
Class::~Class()
""")
ty.add_member('intValue', 'int')
ty.set_default_access(MemberAccess.private)
ty.add_member('floatValue', 'float')
ty.add_const_method('publicConstMethod', 'float')
ty.add_mutable_method('publicMutableMethod', 'float')
ty.add_const_method('publicVoidConstMethod')
ty.add_mutable_method('publicVoidMutableMethod')
ty.add_method('GetStaticFloat', 'float', this_access=ThisAccess.static)\
  .add_test("""
report(Class_GetStaticFloat());
""", """
+3.3
""")
ty.generate_type('Class const &')
ty.add_get_ind_op('int').add_test("""
Class c(-7, 3.14);
report(c.getAt(56));
Class_CxxConstRef cr = c;
report(cr.getAt(56));
""", """
Class::Class(-7, 3.14)
Class::operator[] const(56)
-7
Class::operator[] const(56)
-7
Class::~Class()
""")
ty.add_set_ind_op('int').add_test("""
Class c(-7, 3.14);
c.setAt(56, 4);
report(c);
""", """
Class::Class(-7, 3.14)
Class::operator[](56)
{intValue:4,floatValue:+3.14}
Class::~Class()
""")
ty.add_test("""
Class c(14, -8.9);
report("c.GET_intValue() = " + c.GET_intValue());
report("c.publicConstMethod() = " + c.publicConstMethod());
report("c.publicMutableMethod() = " + c.publicMutableMethod());
Class_CxxConstRef cr = c;
report("cr.GET_intValue() = " + cr.GET_intValue());
report("cr.publicConstMethod() = " + cr.publicConstMethod());
Class_CxxRef mr = Make_Class_CxxRef(c);
report("mr.GET_intValue() = " + mr.GET_intValue());
report("mr.publicConstMethod() = " + mr.publicConstMethod());
report("mr.publicMutableMethod() = " + mr.publicMutableMethod());
Class_CxxConstPtr cp = c;
report("cp.GET_intValue() = " + cp.GET_intValue());
report("cp.publicConstMethod() = " + cp.publicConstMethod());
Class_CxxPtr mp = Make_Class_CxxPtr(c);
report("mp.GET_intValue() = " + mp.GET_intValue());
report("mp.publicConstMethod() = " + mp.publicConstMethod());
report("mp.publicMutableMethod() = " + mp.publicMutableMethod());
""", """
Class::Class(14, -8.9)
c.GET_intValue() = 14
c.publicConstMethod() = -8.9
c.publicMutableMethod() = -8.9
cr.GET_intValue() = 14
cr.publicConstMethod() = -8.9
mr.GET_intValue() = 14
mr.publicConstMethod() = -8.9
mr.publicMutableMethod() = -8.9
cp.GET_intValue() = 14
cp.publicConstMethod() = -8.9
mp.GET_intValue() = 14
mp.publicConstMethod() = -8.9
mp.publicMutableMethod() = -8.9
Class::~Class()
""")
ty.add_test("""
Class c(14, -8.9);
report("c.publicVoidConstMethod()");
c.publicVoidConstMethod();
report("c.publicVoidMutableMethod()");
c.publicVoidMutableMethod();
Class_CxxConstRef cr = c;
report("cr.publicVoidConstMethod()");
cr.publicVoidConstMethod();
Class_CxxRef mr = Make_Class_CxxRef(c);
report("mr.publicVoidConstMethod()");
mr.publicVoidConstMethod();
report("mr.publicVoidMutableMethod()");
mr.publicVoidMutableMethod();
Class_CxxConstPtr cp = c;
report("cp.publicVoidConstMethod()");
cp.publicVoidConstMethod();
Class_CxxPtr mp = Make_Class_CxxPtr(c);
report("mp.publicVoidConstMethod()");
mp.publicVoidConstMethod();
report("mp.publicVoidMutableMethod()");
mp.publicVoidMutableMethod();
""", """
Class::Class(14, -8.9)
c.publicVoidConstMethod()
c.publicVoidMutableMethod()
cr.publicVoidConstMethod()
mr.publicVoidConstMethod()
mr.publicVoidMutableMethod()
cp.publicVoidConstMethod()
mp.publicVoidConstMethod()
mp.publicVoidMutableMethod()
Class::~Class()
""")
ext.add_func('ReturnClass', 'Class')\
  .add_test("""
Class c1 = ReturnClass();
report("ReturnClass: c1 = " + c1);
""", """
Class::Class()
Class::Class(92, 6.74)
Class::operator=(Class const &)
Class::~Class()
ReturnClass: c1 = {intValue:92,floatValue:+6.74}
Class::~Class()
""")

dty = ext.add_in_place_type('DerivedClass', extends='Class')
dty.generate_type('DerivedClass const &')
dty.add_member('shortValue', 'short')
dty.add_ctor(['int', 'float', 'short'])
dty.add_const_method('anotherPublicMethod', 'short')\
  .add_test("""
DerivedClass dc(5, -1e9, 56);
report("dc.shortValue = " + dc.shortValue);
report("dc.publicConstMethod() = " + dc.publicConstMethod());
report("dc.anotherPublicMethod() = " + dc.anotherPublicMethod());
DerivedClass_CxxConstRef dc_cr = dc;
report("dc_cr.GET_shortValue() = " + dc_cr.GET_shortValue());
report("dc_cr.publicConstMethod() = " + dc_cr.publicConstMethod());
report("dc_cr.anotherPublicMethod() = " + dc_cr.anotherPublicMethod());
""", """
Class::Class(5, -1e+09)
DerivedClass::DerivedClass(5, -1e+09, 56)
dc.shortValue = 56
dc.publicConstMethod() = -10.0e8
dc.anotherPublicMethod() = -168
dc_cr.GET_shortValue() = 56
dc_cr.publicConstMethod() = -10.0e8
dc_cr.anotherPublicMethod() = -168
DerivedClass::~DerivedClass()
Class::~Class()
Class::~Class()
""")

#   std::string getDesc() const {
#     char buf[256];
#     snprintf( buf, 256, "intValue:%d floatValue:%f", intValue, floatValue );
#     return std::string( buf );
#   }

# std::vector<Class> ReturnClassVec() {
#   std::vector<Class> result;
#   result.push_back( Class( 3, 3.14 ) );
#   result.push_back( Class( -14, -3.45 ) );
#   return result;
# }
