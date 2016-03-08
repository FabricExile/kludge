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
    this_type_codec,
    members,
    methods,
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
    self.this_type_info = this_type_codec.type_info
    self.const_this = ThisCodec(this_type_codec, False)
    self.mutable_this = ThisCodec(this_type_codec, True)
    self.members = members
    self.methods = methods
    self._template_basename = template_basename

  def jinja_stream(self, jinjenv, lang):
    return jinjenv.get_template(self._template_basename + '.template.' + lang).stream(decl = self)
