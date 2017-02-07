#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('OwnedType.hpp')

ty = ext.add_owned_type('Class')
ty.add_comment("""/// Test comment""")
ty.set_default_visibility(Visibility.public)
ty.add_member('floatValue', 'float')
ty.add_member('stringValue', 'std::string')
ty.set_default_visibility(Visibility.private)
ty.add_member('pri_intValue', 'int')

ty.add_ctor()
ty.add_ctor(['std::string const &'])
ty.add_ctor(['float', 'char const *', 'int'])\
  .add_comment("""Another comment""")\
  .add_test("""
Class c(3.14, "hello", 42);
report("c.cxx_get_floatValue() = " + c.cxx_get_floatValue());
report("c.get_floatValue() = " + c.get_floatValue());
report("c.cxx_get_stringValue() = " + c.cxx_get_stringValue());
report("c.get_stringValue() = " + c.get_stringValue());
c.cxx_set_floatValue(1.23);
report("after c.cxx_set_floatValue(1.23):");
report("c.cxx_get_floatValue() = " + c.cxx_get_floatValue());
report("c.get_floatValue() = " + c.get_floatValue());
c.set_floatValue(-9.67);
report("after c.set_floatValue(-9.67):");
report("c.cxx_get_floatValue() = " + c.cxx_get_floatValue());
report("c.get_floatValue() = " + c.get_floatValue());
""", """
Class::Class(3.14, hello, 42)
c.cxx_get_floatValue() = +3.14
c.get_floatValue() = +3.14
c.cxx_get_stringValue() = hello
c.get_stringValue() = hello
after c.cxx_set_floatValue(1.23):
c.cxx_get_floatValue() = +1.23
c.get_floatValue() = +1.23
after c.set_floatValue(-9.67):
c.cxx_get_floatValue() = -9.67
c.get_floatValue() = -9.67
Class::~Class()
""")
ty.add_mutable_method('publicMethod', 'std::string const &')\
  .add_test("""
Class c(3.14, "hello", 42);
report("c.cxx_publicMethod() = " + c.cxx_publicMethod());
report("c.publicMethod() = " + c.publicMethod());
""", """
Class::Class(3.14, hello, 42)
c.cxx_publicMethod() = hello
c.publicMethod() = hello
Class::~Class()
""")

ty.add_const_method('data', 'int')\
  .add_test("""
Class c(5.1, 'baz', 3);
report("c.cxx_data() = " + c.cxx_data());
report("c.data_() = " + c.data_());
""", """
Class::Class(5.1, baz, 3)
c.cxx_data() = 432
c.data_() = 432
Class::~Class()
""")

ty.add_static_method('PrintValues', None, ['Class const &'])\
  .add_test("""
Class c(1.32, "hoo", 23);
Class_CxxPrintValues(c);
Class_PrintValues(c);
""", """
Class::Class(1.32, hoo, 23)
1.32 hoo 23
1.32 hoo 23
Class::~Class()
""")

ty.add_test("""
Class c1(3.14, "hello", 42);
Class c2 = c1;
c1 = c2;
""", """
Class::Class(3.14, hello, 42)
Class::Class(Class const &)
Class::operator=(Class const &)
Class::~Class()
Class::~Class()
""")

ty.add_cast('bool')\
  .add_test("""
Class c1(3.14, "hello", 4);
report(!!c1);
Class c2(3.14, "hello", 0);
report(!!c2);
""", """
Class::Class(3.14, hello, 4)
true
Class::Class(3.14, hello, 0)
false
Class::~Class()
Class::~Class()
""")

ty.add_uni_op('++', 'bool', kl_method_name='next')
ty.add_deref('int const &')
ty.add_test("""
for ( Class c1(3.14, "hello", -2); c1; c1.next() )
  report(c1.cxx_deref());
""", """
Class::Class(3.14, hello, -2)
-2
-1
Class::~Class()
""")

ty.add_bin_op('+', 'Class', ['Class const &', 'Class const &'])\
  .add_test("""
Class c1(5.4, "one", -7);
report("c1 = " + c1);
report("c1+c1 = " + (c1+c1));
""", """
Class::Class(5.4, one, -7)
c1 = Class:{floatValue:+5.4,stringValue:one}
Class::Class(10.8, oneone, -14)
c1+c1 = Class:{floatValue:+10.8,stringValue:oneone}
Class::~Class()
Class::~Class()
""")

ty.add_ass_op('+=', ['Class const &'])\
  .add_test("""
Class c1(5.4, "one", -7);
report("c1 = " + c1);
c1 += c1;
report("c1 = " + c1);
""", """
Class::Class(5.4, one, -7)
c1 = Class:{floatValue:+5.4,stringValue:one}
Class::Class(10.8, oneone, -14)
Class::operator=(Class const &)
Class::~Class()
c1 = Class:{floatValue:+10.8,stringValue:oneone}
Class::~Class()
""")

ext.add_bin_op('*', 'Class', ['Class const &', 'Class const &'])\
  .add_test("""
Class c1(5.4, "one", -7);
report("c1 = " + c1);
report("c1 * c1 = " + (c1 * c1));
""", """
Class::Class(5.4, one, -7)
c1 = Class:{floatValue:+5.4,stringValue:one}
Class::Class(29.16, oneone, 49)
c1 * c1 = Class:{floatValue:+29.16,stringValue:oneone}
Class::~Class()
Class::~Class()
""")

ext.add_func('GlobalFuncTakingClassConstRef', None, ['Class const &'])\
  .add_test("""
CxxGlobalFuncTakingClassConstRef("hello");
GlobalFuncTakingClassConstRef("hello");
""", """
Class::Class(hello)
Class::Class(Class const &)
Class::~Class()
GlobalFuncTakingClassConstRef: klass.stringValue = hello
Class::~Class()
Class::Class(hello)
GlobalFuncTakingClassConstRef: klass.stringValue = hello
Class::~Class()
""")

ty.add_call_op(None, ['int'])\
  .add_test("""
Class cl(1.1, "foo", -8);
cl.cxx_call(14);
""", """
Class::Class(1.1, foo, -8)
Class::operator()(14)
Class::~Class()
""")

dty = ext.add_owned_type('DerivedClass', extends='Class')
dty.add_ctor(['int'])
dty.add_const_method('newMethod', 'int')
dty.add_member('newPublicMember', 'double', visibility=Visibility.public)
dty.add_test("""
DerivedClass dc(56);
report("dc = " + dc);
report("dc.cxx_newMethod() = " + dc.cxx_newMethod());
report("dc.cxx_publicMethod() = " + dc.cxx_publicMethod());
Class c = dc;
report("c = " + c);
report("c.cxx_publicMethod() = " + c.cxx_publicMethod());
""", """
Class::Class(3.14, hello, 56)
DerivedClass::DerivedClass(56)
dc = DerivedClass:{floatValue:+3.14,stringValue:hello,newPublicMember:+2.81}
dc.cxx_newMethod() = -9
dc.cxx_publicMethod() = hello
Class::Class(Class const &)
c = Class:{floatValue:+3.14,stringValue:hello}
c.cxx_publicMethod() = hello
Class::~Class()
DerivedClass::~DerivedClass()
Class::~Class()
""")

#   void changeValues( Class &that )
#   {
#     floatValue = that.floatValue;
#     stringValue = that.stringValue;
#     pri_intValue = that.pri_intValue;
#   }

#   std::string const &publicMethod() { return stringValue; }

#   std::string getDesc() const {
#     return "stringValue: " + stringValue;
#   }

#   float getMulFloatValue( float x ) const { return x * floatValue; }

#   void exportValues(
#     float &_floatValue,
#     std::string &_stringValue,
#     int &_intValue
#     )
#   {
#     _floatValue = floatValue;
#     _stringValue = stringValue;
#     _intValue = pri_intValue;
#   }

# protected:

#   std::string const &protectedMethod() { return stringValue; }

# private:

#   std::string const &privateMethod() { return stringValue; }

# public:

#   float floatValue;
#   std::string stringValue;

# private:

#   int pri_intValue;
# };

# Class ReturnClass() {
#   return Class( 5.61, "foo", -43 );
# }

# std::vector<Class> ReturnClassVec() {
#   std::vector<Class> result;
#   result.push_back( Class( 1.2, "bar", 64 ) );
#   result.push_back( Class( -97.1, "baz", 164 ) );
#   return result;
# }

# struct StructWithIndirectTypeThatCanInPlace {
#   StructWithIndirectTypeThatCanInPlace( float const &x )
#     : floatValue( x ) {}
#   float const &floatValue;
# };

# StructWithIndirectTypeThatCanInPlace ReturnStructWithIndirectTypeThatCanInPlace() {
#   static float x = 5.76;
#   return StructWithIndirectTypeThatCanInPlace( x );
# }


# require WrappedPtr;

# operator entry() {
#   Class value;
#   report("ReturnClass() = " + ReturnClass());
#   report("ReturnClassVec() = " + ReturnClassVec());

#   value = ReturnClass();
#   report("Before value.cxx_set_floatValue(-12.34): value.cxx_get_floatValue() = " + value.cxx_get_floatValue());
#   value.cxx_set_floatValue(-12.34);
#   report("After value.cxx_set_floatValue(-12.34): value.cxx_get_floatValue() = " + value.cxx_get_floatValue());
#   report("Before value.cxx_set_stringValue('hello'): value.cxx_get_stringValue() = " + value.cxx_get_stringValue());
#   value.cxx_set_stringValue('hello');
#   report("After value.cxx_set_stringValue('hello'): value.cxx_get_stringValue() = " + value.cxx_get_stringValue());

#   report("value.publicMethod() = " + value.publicMethod());
#   report("value.getDesc() = " + value.getDesc());
#   report("value.getMulFloatValue(5.12) = " + value.getMulFloatValue(5.12));

#   Float32 floatValue;
#   String stringValue;
#   SInt32 intValue;
#   value.exportValues(floatValue, stringValue, intValue);
#   report("value.exportValues(...): floatValue = " + floatValue);
#   report("value.exportValues(...): stringValue = " + stringValue);
#   report("value.exportValues(...): intValue = " + intValue);

#   StructWithIndirectTypeThatCanInPlace st =
#     ReturnStructWithIndirectTypeThatCanInPlace();
#   report("st.cxx_get_floatValue() = " + st.cxx_get_floatValue());

#   Class constructor1(1.1, 'myString', 123);
#   constructor1.exportValues(floatValue, stringValue, intValue);
#   report("value.exportValues(...): floatValue = " + floatValue);
#   report("value.exportValues(...): stringValue = " + stringValue);
#   report("value.exportValues(...): intValue = " + intValue);

#   Class constructor2(constructor1);
#   constructor2.exportValues(floatValue, stringValue, intValue);
#   report("value.exportValues(...): floatValue = " + floatValue);
#   report("value.exportValues(...): stringValue = " + stringValue);
#   report("value.exportValues(...): intValue = " + intValue);

#   Class c3(2.2, 'otherString', 456);
#   Class_PrintValues(c3);
#   c3.changeValues(constructor2);
#   Class_PrintValues(c3);
# }
