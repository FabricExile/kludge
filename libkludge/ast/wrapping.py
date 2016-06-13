#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from decl import Decl
from libkludge.value_name import this_cpp_value_name
from libkludge.this_codec import ThisCodec

class Wrapping(Decl):
  def __init__(
    self,
    extname,
    include_filename,
    location,
    desc,
    this_type_info,
    members,
    methods,
    constructors,
    base_classes,
    block_empty_kl_constructor,
    template_basename,
    ):
    Decl.__init__(
        self,
        extname,
        include_filename,
        location,
        desc,
        )
    self.this_value_name = this_cpp_value_name
    self.this_type_info = this_type_info
    self.const_this = ThisCodec(this_type_info, False)
    self.mutable_this = ThisCodec(this_type_info, True)
    self.members = members
    self.methods = methods
    self.constructors = constructors
    self.base_classes = base_classes
    self.block_empty_kl_constructor = block_empty_kl_constructor
    self._template_basename = template_basename

  def jinja_stream(self, jinjenv, lang):
    return jinjenv.get_template(self._template_basename + '.template.' + lang).stream(decl = self)
