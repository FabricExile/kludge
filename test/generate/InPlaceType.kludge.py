#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('InPlaceType.hpp')

ty = ext.add_in_place_type('Class')
ty.add_ctor()
ty.add_ctor(['int', 'float']).add_test("""
Class c(-7, 1.52);
report("c.get_intValue() = " + c.get_intValue());
""", """
Class::Class(-7, 1.52)
c.get_intValue() = -7
Class::~Class()
""")
ty.add_member('intValue', 'int')
ty.set_default_access(MemberAccess.private)
ty.add_member('floatValue', 'float')
ty.add_method('GetStaticFloat', 'float', this_access=ThisAccess.static)\
  .add_test("""
report(Class_GetStaticFloat());
""", """
+3.3
""")
ty.add_get_ind_op('int').add_test("""
Class c(-7, 3.14);
report(c.getAt(56));
""", """
Class::Class(-7, 3.14)
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

#   Class( Class const &that )
#     : intValue( that.intValue ), floatValue( that.floatValue )
#     {}

#   Class &operator=( Class const &that )
#   {
#     intValue = that.intValue;
#     floatValue = that.floatValue;
#     return *this;
#   }

#   float publicMethod() { return floatValue; }

#   std::string getDesc() const {
#     char buf[256];
#     snprintf( buf, 256, "intValue:%d floatValue:%f", intValue, floatValue );
#     return std::string( buf );
#   }

# protected:

#   float protectedMethod() { return floatValue; }

# private:

#   float privateMethod() { return floatValue; }

# public:

#   int intValue;

# private:

#   float floatValue;
# };

# Class ReturnClass() {
#   return Class( 92, 6.74 );
# }

# std::vector<Class> ReturnClassVec() {
#   std::vector<Class> result;
#   result.push_back( Class( 3, 3.14 ) );
#   result.push_back( Class( -14, -3.45 ) );
#   return result;
# }

# #endif
# require InPlaceStruct;

# operator entry() {
#   Class value;
#   report("ReturnClass() = " + ReturnClass());
#   report("ReturnClassVec() = " + ReturnClassVec());
#   value = ReturnClass();
#   report("value.intValue = " + value.intValue);
#   report("value.getDesc() = " + value.getDesc());
#   Class constructor1(1, 2.2);
#   report("constructor1.getDesc() = " + constructor1.getDesc());
#   Class constructor2(constructor1);
#   report("constructor2.getDesc() = " + constructor2.getDesc());
#   report("Class::GetStaticFloat() = " + Class_GetStaticFloat());
# }
