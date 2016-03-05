from decl import Decl
from libkludge.value_name import ValueName

class Wrapping(Decl):
  def __init__(
    self,
    extname,
    include_filename,
    location,
    desc,
    type_mgr,
    self_type_name,
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
    self.self_type_name = type_mgr.get_type_info(self_type_name)
    self.self_codec_const = type_mgr.get_type_info(self_type_name + " const &").make_codec(ValueName("RESERVED_self"))
    self.self_codec_mutable = type_mgr.get_type_info(self_type_name + " &").make_codec(ValueName("RESERVED_self"))
    self.members = members
    self.methods = methods
    self._template_basename = template_basename

  def jinja_stream(self, jinjenv, lang):
    return jinjenv.get_template(self._template_basename + '.template.' + lang).stream(decl = self)
