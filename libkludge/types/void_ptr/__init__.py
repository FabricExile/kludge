#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from libkludge.type_info import TypeInfo
from libkludge.selector import Selector
from libkludge.dir_qual_type_info import DirQualTypeInfo
from libkludge.cpp_type_expr_parser import *
from libkludge.generate.builtin_decl import BuiltinDecl

const_cpp_type_expr = PointerTo(Const(Void()))
mutable_cpp_type_expr = PointerTo(Void())

class ConstVoidPtrTypeInfo(TypeInfo):

  def __init__(self, jinjenv):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base='Data',
      edk_name='Fabric::EDK::KL::Data',
      lib_expr=const_cpp_type_expr,
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "protocols/conv/builtin/none_cast_away_const"
    tds["result"]["*"] = "protocols/result/builtin/direct"
    tds["repr"]["new_begin"] = "types/builtin/void_ptr/repr"
    tds["repr"]["new_end"] = "types/builtin/void_ptr/repr"
    return tds

class MutableVoidPtrTypeInfo(TypeInfo):

  def __init__(self, jinjenv):
    TypeInfo.__init__(
      self,
      jinjenv,
      kl_name_base='Data',
      edk_name='Fabric::EDK::KL::Data',
      lib_expr=mutable_cpp_type_expr,
      )

  def build_codec_lookup_rules(self):
    tds = TypeInfo.build_codec_lookup_rules(self)
    tds["conv"]["*"] = "protocols/conv/builtin/none"
    tds["result"]["*"] = "protocols/result/builtin/direct"
    tds["repr"]["new_begin"] = "types/builtin/void_ptr/repr"
    tds["repr"]["new_end"] = "types/builtin/void_ptr/repr"
    return tds

class VoidPtrDecl(BuiltinDecl):

  def __init__(self, ext):
    BuiltinDecl.__init__(
      self,
      ext.root_namespace,
      desc="VoidPtr",
      template_path="types/builtin/void_ptr/void_ptr",
      test_name="VoidPtr",
      )

  def render_method_impls(self, lang):
    return self.type_info.record.render('impls', lang, {
      })

class VoidPtrSelector(Selector):

  def __init__(self, ext):
    Selector.__init__(self, ext)
    self.have_decl = False

  def get_desc(self):
    return "VoidPtr"

  def maybe_create_dqti(self, type_mgr, cpp_type_expr):
    if cpp_type_expr == const_cpp_type_expr:
      dqti = DirQualTypeInfo(
        dir_qual.direct,
        ConstVoidPtrTypeInfo(self.jinjenv)
        )
      if not self.have_decl:
        self.ext.add_decl(VoidPtrDecl(self.ext))
        self.have_decl = True
      return dqti
    if cpp_type_expr == mutable_cpp_type_expr:
      dqti = DirQualTypeInfo(
        dir_qual.direct,
        MutableVoidPtrTypeInfo(self.jinjenv)
        )
      if not self.have_decl:
        self.ext.add_decl(VoidPtrDecl(self.ext))
        self.have_decl = True
      return dqti
