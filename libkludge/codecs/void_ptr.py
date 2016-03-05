from libkludge.codec import Codec
from libkludge.type_spec import SimpleTypeSpec
from libkludge.gen_spec import GenLambda, GenStr, GenLambda
from libkludge.cpp_type_expr_parser import *

def build_void_ptr_codecs():
  class VoidPtrBaseCodec(Codec): pass
  VoidPtrBaseCodec.traits_value()
  VoidPtrBaseCodec.conv_none()
  VoidPtrBaseCodec.result_direct()
  VoidPtrBaseCodec.prop_in_place()

  class ConstVoidPtrCodec(VoidPtrBaseCodec): pass
  ConstVoidPtrCodec.match_cpp_type_expr(
    PointerTo(Const(Void())),
    SimpleTypeSpec.builder('Data', 'void const *')
    )
  ConstVoidPtrCodec.traits_value()
  ConstVoidPtrCodec.conv_none_cast_away_const()
  ConstVoidPtrCodec.result_direct()

  class MutableVoidPtrCodec(VoidPtrBaseCodec): pass
  MutableVoidPtrCodec.match_cpp_type_expr(
    PointerTo(Void()),
    SimpleTypeSpec.builder('Data', 'void *')
    )
  MutableVoidPtrCodec.traits_value()
  MutableVoidPtrCodec.conv_none()
  MutableVoidPtrCodec.result_direct()

  return [
    ConstVoidPtrCodec,
    MutableVoidPtrCodec,
    ]
