from libkludge.codec import Codec
from libkludge.gen_spec import GenStr, GenLambda
from libkludge.type_spec import SimpleTypeSpec
from libkludge.cpp_type_expr_parser import *

def build_in_place_struct_codecs(class_name):
  class InPlaceStructCodecBase(Codec): pass
  InPlaceStructCodecBase.conv_none()
  InPlaceStructCodecBase.result(
    decl_and_assign_cpp = GenLambda(
      lambda self: self.name.edk + " = " + self.traits_pointer_undo()
      ),
    indirect_assign_to_edk = GenStr(""),
    )
  class InPlaceStructValueCodec(InPlaceStructCodecBase): pass
  InPlaceStructValueCodec.match_cpp_type_expr(
    Named(class_name),
    SimpleTypeSpec.builder(class_name, class_name)
    )
  InPlaceStructValueCodec.traits_value()
  InPlaceStructValueCodec.prop_in_place()

  class InPlaceStructConstRefCodec(InPlaceStructCodecBase): pass
  InPlaceStructConstRefCodec.match_cpp_type_expr(
    ReferenceTo(Const(Named(class_name))),
    SimpleTypeSpec.builder(class_name, class_name)
    )
  InPlaceStructConstRefCodec.traits_const_ref()

  class InPlaceStructConstPtrCodec(InPlaceStructCodecBase): pass
  InPlaceStructConstPtrCodec.match_cpp_type_expr(
    PointerTo(Const(Named(class_name))),
    SimpleTypeSpec.builder(class_name, class_name)
    )
  InPlaceStructConstPtrCodec.traits_const_ptr()

  class InPlaceStructMutableRefType(InPlaceStructCodecBase): pass
  InPlaceStructMutableRefType.match_cpp_type_expr(
    ReferenceTo(Named(class_name)),
    SimpleTypeSpec.builder(class_name, class_name)
    )
  InPlaceStructMutableRefType.traits_mutable_ref()
  InPlaceStructMutableRefType.param_io()

  class InPlaceStructMutablePtrType(InPlaceStructCodecBase): pass
  InPlaceStructMutablePtrType.match_cpp_type_expr(
    PointerTo(Named(class_name)),
    SimpleTypeSpec.builder(class_name, class_name)
    )
  InPlaceStructMutablePtrType.traits_mutable_ptr()
  InPlaceStructMutablePtrType.param_io()

  return [
    InPlaceStructValueCodec,
    InPlaceStructConstRefCodec,
    InPlaceStructConstPtrCodec,
    InPlaceStructMutableRefType,
    InPlaceStructMutablePtrType,
    ]
