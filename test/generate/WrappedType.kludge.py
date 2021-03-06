#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('WrappedType.hpp')

ty = ext.add_wrapped_type('Wrapper', 'Class')
ty.add_ctor(['float', 'char const *', 'int'])
ty.set_default_visibility(Visibility.public)
ty.add_member('floatValue', 'float')
ty.add_member('stringValue', 'std::string')
ty.set_default_visibility(Visibility.private)
ty.add_member('pri_intValue', 'int')
ty.add_test("""
Class c(3.14, "hello", 42);
report("c.cxx_get_floatValue() = " + c.cxx_get_floatValue());
report("c.cxx_get_stringValue() = " + c.cxx_get_stringValue());
""", """
Class::Class(3.14, hello, 42)
Wrapper::Wrapper(Ty *)
c.cxx_get_floatValue() = +3.14
c.cxx_get_stringValue() = hello
Wrapper::~Wrapper()
Class::~Class()
""")
ty.add_mutable_method('publicMethod', 'std::string const &')\
  .add_test("""
Class c(3.14, "hello", 42);
report("c.cxx_publicMethod() = " + c.cxx_publicMethod());
report("c.publicMethod() = " + c.publicMethod());
""", """
Class::Class(3.14, hello, 42)
Wrapper::Wrapper(Ty *)
c.cxx_publicMethod() = hello
c.publicMethod() = hello
Wrapper::~Wrapper()
Class::~Class()
""")
ty.add_const_method('unwrap', 'Class const *')
ty.add_static_method('PrintValues', None, ['Class const *'])
ty.add_test("""
Class c(1.32, "hoo", 23);
CxxClassConstPtr ptr = c.cxx_unwrap();
Class_CxxPrintValues(ptr);
""", """
Class::Class(1.32, hoo, 23)
Wrapper::Wrapper(Ty *)
1.32 hoo 23
Wrapper::~Wrapper()
Class::~Class()
""")
ty.add_test("""
Class c(1.32, "hoo", 23);
CxxRawClass ptr = c.unwrap();
CxxRawClass_CxxPrintValues(ptr);
""", """
Class::Class(1.32, hoo, 23)
Wrapper::Wrapper(Ty *)
Wrapper::Wrapper(Ty *)
Wrapper::Wrapper(Ty *)
Wrapper::~Wrapper()
Wrapper::~Wrapper()
1.32 hoo 23
Wrapper::~Wrapper()
Class::~Class()
""")
ty.add_static_method('PrintValues', None, ['Wrapper<Class> const &'])
ty.add_test("""
Class_CxxPrintValues(Make_CxxWrappedClassConstRef(Class(1.32, "hoo", 23)));
""", """
Class::Class(1.32, hoo, 23)
Wrapper::Wrapper(Ty *)
1.32 hoo 23
Wrapper::~Wrapper()
Class::~Class()
""")
ty.add_test("""
Class_PrintValues(Class(1.32, "hoo", 23));
""", """
Class::Class(1.32, hoo, 23)
Wrapper::Wrapper(Ty *)
1.32 hoo 23
Wrapper::~Wrapper()
Class::~Class()
""")
ty.add_get_ind_op('int').add_test("""
Class c(3.14, "foo", -7);
report(c.cxx_getAtIndex(56));
""", """
Class::Class(3.14, foo, -7)
Wrapper::Wrapper(Ty *)
Class::operator[] const(56)
-7
Wrapper::~Wrapper()
Class::~Class()
""")
ty.add_set_ind_op('int').add_test("""
Class c(3.14, "foo", -7);
c.cxx_setAtIndex(56, 4);
report(c);
""", """
Class::Class(3.14, foo, -7)
Wrapper::Wrapper(Ty *)
Class::operator[](56)
{cpp_ptr:<Opaque>}
Wrapper::~Wrapper()
Class::~Class()
""")

ty = ext.add_wrapped_type('Wrapper', 'DerivedClass', extends='Class')
ty.add_ctor(['int'])
ty.add_const_method('newMethod', 'int')
ty.add_test("""
DerivedClass dc(56);
report("dc.cxx_newMethod() = " + dc.cxx_newMethod());
report("dc.cxx_publicMethod() = " + dc.cxx_publicMethod());
Class c = dc;
report("c.cxx_publicMethod() = " + c.cxx_publicMethod());
""", """
Class::Class(3.14, hello, 56)
DerivedClass::DerivedClass(56)
Wrapper::Wrapper(Ty *)
dc.cxx_newMethod() = -9
dc.cxx_publicMethod() = hello
Wrapper::Wrapper(Ty *)
c.cxx_publicMethod() = hello
Wrapper::~Wrapper()
Wrapper::~Wrapper()
DerivedClass::~DerivedClass()
Class::~Class()
""")
ty.add_test("""
DerivedClass dc(56);
report("dc.newMethod() = " + dc.newMethod());
report("dc.publicMethod() = " + dc.publicMethod());
Class c = dc;
report("c.publicMethod() = " + c.publicMethod());
""", """
Class::Class(3.14, hello, 56)
DerivedClass::DerivedClass(56)
Wrapper::Wrapper(Ty *)
dc.newMethod() = -9
dc.publicMethod() = hello
Wrapper::Wrapper(Ty *)
c.publicMethod() = hello
Wrapper::~Wrapper()
Wrapper::~Wrapper()
DerivedClass::~DerivedClass()
Class::~Class()
""")

ext.add_func("GetWrappedClass", "Wrapper<Class>", [])
ext.add_test("""
report(GetWrappedClass());
""", """
Class::Class(6.72, asjdbf, -54)
Wrapper::Wrapper(Ty *)
Wrapper::Wrapper(Wrapper const &)
Wrapper::~Wrapper()
Wrapper::Wrapper(Ty *)
Wrapper::~Wrapper()
{cpp_ptr:<Opaque>}
Wrapper::~Wrapper()
Class::~Class()
""")

ext.add_func("GlobalGetIntValue", "int", ["Class const &"])
#  !!!! THIS WILL THROW EXCEPTION, MUST BE LAST !!!!
ext.add_test("""
Class klass;
report(GlobalGetIntValue(klass));
""", """
Error: WrappedType: dereferenced null Class const & pointer
KL stack trace:
""", skip_epilog=True)

#   Class() {}
#   Class(
#     float _floatValue,
#     std::string const &_stringValue,
#     int _intValue
#     )
#     : floatValue( _floatValue )
#     , stringValue( _stringValue )
#     , pri_intValue( _intValue )
#     {}
#   Class( Class const &that )
#     : floatValue( that.floatValue )
#     , stringValue( that.stringValue )
#     , pri_intValue( that.pri_intValue )
#     {}
#   ~Class() {}

#   Class &operator=( Class const &that )
#   {
#     floatValue = that.floatValue;
#     stringValue = that.stringValue;
#     pri_intValue = that.pri_intValue;
#     return *this;
#   }

#   static void PrintValues( Class const &that )
#   {
#     printf("%.2f %s %d\n", that.floatValue, that.stringValue.c_str(),
#            that.pri_intValue);
#   }

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
