from kludge import TypeCodec, GenStr, GenLambda, SimpleTypeSpec
from kludge.CPPTypeExpr import *

def build_in_place_struct_type_codecs(class_name):
  class InPlaceStructTypeCodecBase(TypeCodec): pass
  InPlaceStructTypeCodecBase.conv_none()
  InPlaceStructTypeCodecBase.result(
    decl_and_assign_cpp = GenLambda(
      lambda self: self.name.edk + " = " + self.traits_pointer_undo()
      ),
    indirect_assign_to_edk = GenStr(""),
    )
  class InPlaceStructValueTypeCodec(InPlaceStructTypeCodecBase): pass
  InPlaceStructValueTypeCodec.match_cpp_type_expr(
    Named(class_name),
    SimpleTypeSpec.builder(class_name, class_name)
    )
  InPlaceStructValueTypeCodec.traits_value()
  InPlaceStructValueTypeCodec.prop_in_place()

  class InPlaceStructConstRefTypeCodec(InPlaceStructTypeCodecBase): pass
  InPlaceStructConstRefTypeCodec.match_cpp_type_expr(
    ReferenceTo(Const(Named(class_name))),
    SimpleTypeSpec.builder(class_name, class_name)
    )
  InPlaceStructConstRefTypeCodec.traits_const_ref()

  class InPlaceStructConstPtrTypeCodec(InPlaceStructTypeCodecBase): pass
  InPlaceStructConstRefTypeCodec.match_cpp_type_expr(
    PointerTo(Const(Named(class_name))),
    SimpleTypeSpec.builder(class_name, class_name)
    )
  InPlaceStructConstPtrTypeCodec.traits_const_ptr()

  class InPlaceStructMutableRefType(InPlaceStructTypeCodecBase): pass
  InPlaceStructConstRefTypeCodec.match_cpp_type_expr(
    ReferenceTo(Named(class_name)),
    SimpleTypeSpec.builder(class_name, class_name)
    )
  InPlaceStructMutableRefType.traits_mutable_ref()
  InPlaceStructMutableRefType.param_io()

  class InPlaceStructMutablePtrType(InPlaceStructTypeCodecBase): pass
  InPlaceStructConstRefTypeCodec.match_cpp_type_expr(
    PointerTo(Named(class_name)),
    SimpleTypeSpec.builder(class_name, class_name)
    )
  InPlaceStructMutablePtrType.traits_mutable_ptr()
  InPlaceStructMutablePtrType.param_io()

  return [
    InPlaceStructValueTypeCodec,
    InPlaceStructConstRefTypeCodec,
    InPlaceStructConstPtrTypeCodec,
    InPlaceStructMutableRefType,
    InPlaceStructMutablePtrType,
    ]
