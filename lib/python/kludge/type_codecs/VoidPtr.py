from kludge import TypeCodec, GenLambda, SimpleTypeSpec, GenStr, GenLambda
from kludge.CPPTypeExpr import *

def build_void_ptr_type_codecs():
  class VoidPtrBaseTypeCodec(TypeCodec): pass
  VoidPtrBaseTypeCodec.traits_value()
  VoidPtrBaseTypeCodec.conv_none()
  VoidPtrBaseTypeCodec.result_direct()
  VoidPtrBaseTypeCodec.prop_in_place()

  class ConstVoidPtrTypeCodec(VoidPtrBaseTypeCodec): pass
  ConstVoidPtrTypeCodec.match_cpp_type_expr(
    PointerTo(Const(Void())),
    SimpleTypeSpec.builder('Data', 'void const *')
    )
  ConstVoidPtrTypeCodec.traits_value()
  ConstVoidPtrTypeCodec.conv_none_cast_away_const()
  ConstVoidPtrTypeCodec.result_direct()

  class MutableVoidPtrTypeCodec(VoidPtrBaseTypeCodec): pass
  MutableVoidPtrTypeCodec.match_cpp_type_expr(
    PointerTo(Void()),
    SimpleTypeSpec.builder('Data', 'void *')
    )
  MutableVoidPtrTypeCodec.traits_value()
  MutableVoidPtrTypeCodec.conv_none()
  MutableVoidPtrTypeCodec.result_direct()

  return [
    ConstVoidPtrTypeCodec,
    MutableVoidPtrTypeCodec,
    ]
