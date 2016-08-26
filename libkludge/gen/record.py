#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from decl import Decl
from libkludge.value_name import this_cpp_value_name
from libkludge.this_codec import ThisCodec

class Record(Decl):
  def __init__(
    self,
    ext,
    desc,
    kl_type_name,
    this_type_info,
    base_classes,
    template_basename,
    block_empty_ctor = False
    ):
    Decl.__init__(self, ext, desc)
    
    self.kl_type_name = kl_type_name
    self.this_value_name = this_cpp_value_name
    self.this_type_info = this_type_info
    self.const_this = ThisCodec(this_type_info, False)
    self.mutable_this = ThisCodec(this_type_info, True)
    self.base_classes = base_classes
    self.template_basename = template_basename
    self.block_empty_ctor = block_empty_ctor

    self.ctors = []
    self.members = []
    self.methods = []

  def get_kl_name(self):
    return self.kl_type_name

  def get_template_basename(self):
    return self.template_basename
