#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('InPlaceType.hpp')

ty = ext.add_in_place_type('Class')
ty.add_ctor()
ty.add_ctor(['int', 'float']).add_test("""
Class c(-7, 1.52);
report("c.intValue = " + c.intValue);
report("c.cxx_get_intValue() = " + c.cxx_get_intValue());
""", """
Class::Class(-7, 1.52)
c.intValue = -7
c.cxx_get_intValue() = -7
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
ty.set_default_visibility(Visibility.private)
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
report(c.cxx_getAtIndex(56));
CxxClassConstRef cr = c;
report(cr.cxx_getAtIndex(56));
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
c.cxx_setAtIndex(56, 4);
report(c);
""", """
Class::Class(-7, 3.14)
Class::operator[](56)
{intValue:4,floatValue:+3.14}
Class::~Class()
""")
ty.add_test("""
Class c(14, -8.9);
report("c.cxx_get_intValue() = " + c.cxx_get_intValue());
report("c.publicConstMethod() = " + c.publicConstMethod());
report("c.publicMutableMethod() = " + c.publicMutableMethod());
CxxClassConstRef cr = c;
report("cr.cxx_get_intValue() = " + cr.cxx_get_intValue());
report("cr.cxx_publicConstMethod() = " + cr.cxx_publicConstMethod());
CxxClassRef mr = Make_CxxClassRef(c);
report("mr.cxx_get_intValue() = " + mr.cxx_get_intValue());
report("mr.cxx_publicConstMethod() = " + mr.cxx_publicConstMethod());
report("mr.cxx_publicMutableMethod() = " + mr.cxx_publicMutableMethod());
CxxClassConstPtr cp = c;
report("cp.cxx_get_intValue() = " + cp.cxx_get_intValue());
report("cp.cxx_publicConstMethod() = " + cp.cxx_publicConstMethod());
CxxClassPtr mp = Make_CxxClassPtr(c);
report("mp.cxx_get_intValue() = " + mp.cxx_get_intValue());
report("mp.cxx_publicConstMethod() = " + mp.cxx_publicConstMethod());
report("mp.cxx_publicMutableMethod() = " + mp.cxx_publicMutableMethod());
""", """
Class::Class(14, -8.9)
c.cxx_get_intValue() = 14
c.publicConstMethod() = -8.9
c.publicMutableMethod() = -8.9
cr.cxx_get_intValue() = 14
cr.cxx_publicConstMethod() = -8.9
mr.cxx_get_intValue() = 14
mr.cxx_publicConstMethod() = -8.9
mr.cxx_publicMutableMethod() = -8.9
cp.cxx_get_intValue() = 14
cp.cxx_publicConstMethod() = -8.9
mp.cxx_get_intValue() = 14
mp.cxx_publicConstMethod() = -8.9
mp.cxx_publicMutableMethod() = -8.9
Class::~Class()
""")
ty.add_test("""
Class c(14, -8.9);
report("c.publicVoidConstMethod()");
c.publicVoidConstMethod();
report("c.publicVoidMutableMethod()");
c.publicVoidMutableMethod();
CxxClassConstRef cr = c;
report("cr.cxx_publicVoidConstMethod()");
cr.cxx_publicVoidConstMethod();
CxxClassRef mr = Make_CxxClassRef(c);
report("mr.cxx_publicVoidConstMethod()");
mr.cxx_publicVoidConstMethod();
report("mr.cxx_publicVoidMutableMethod()");
mr.cxx_publicVoidMutableMethod();
CxxClassConstPtr cp = c;
report("cp.cxx_publicVoidConstMethod()");
cp.cxx_publicVoidConstMethod();
CxxClassPtr mp = Make_CxxClassPtr(c);
report("mp.cxx_publicVoidConstMethod()");
mp.cxx_publicVoidConstMethod();
report("mp.cxx_publicVoidMutableMethod()");
mp.cxx_publicVoidMutableMethod();
""", """
Class::Class(14, -8.9)
c.publicVoidConstMethod()
c.publicVoidMutableMethod()
cr.cxx_publicVoidConstMethod()
mr.cxx_publicVoidConstMethod()
mr.cxx_publicVoidMutableMethod()
cp.cxx_publicVoidConstMethod()
mp.cxx_publicVoidConstMethod()
mp.cxx_publicVoidMutableMethod()
Class::~Class()
""")
ext.add_func('ReturnClass', 'Class')\
  .add_test("""
Class c1 = ReturnClass();
report("ReturnClass: c1 = " + c1);
""", """
Class::Class()
Class::Class()
Class::Class(92, 6.74)
Class::operator=(Class const &)
Class::~Class()
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
DerivedClass dc(5, -3.14, 56);
report("dc.shortValue = " + dc.shortValue);
report("dc.cxx_publicConstMethod() = " + dc.cxx_publicConstMethod());
report("dc.publicConstMethod() = " + dc.publicConstMethod());
report("dc.cxx_anotherPublicMethod() = " + dc.cxx_anotherPublicMethod());
report("dc.anotherPublicMethod() = " + dc.anotherPublicMethod());
CxxDerivedClassConstRef dc_cr = dc;
report("dc_cr.cxx_get_shortValue() = " + dc_cr.cxx_get_shortValue());
report("dc_cr.cxx_publicConstMethod() = " + dc_cr.cxx_publicConstMethod());
report("dc_cr.cxx_anotherPublicMethod() = " + dc_cr.cxx_anotherPublicMethod());
""", """
Class::Class()
Class::Class(5, -3.14)
DerivedClass::DerivedClass(5, -3.14, 56)
dc.shortValue = 56
dc.cxx_publicConstMethod() = -3.14
dc.publicConstMethod() = -3.14
dc.cxx_anotherPublicMethod() = -168
dc.anotherPublicMethod() = -168
dc_cr.cxx_get_shortValue() = 56
dc_cr.cxx_publicConstMethod() = -3.14
dc_cr.cxx_anotherPublicMethod() = -168
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
