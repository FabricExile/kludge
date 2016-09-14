#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from symbol_helpers import replace_invalid_chars
from libkludge.generate.record import Record

class KLTypeName:

  def __init__(self, base, suffix):
    self.base = base
    self.suffix = suffix

  @property
  def compound(self):
    return self.base + self.suffix

  def __str__(self):
    return self.compound

class KLTypeInfo:

  def __init__(self, name_base, name_suffix):
    self.name = KLTypeName(name_base, name_suffix)

class EDKTypeInfo:

  def __init__(self, name):
    self.name = name

class LibTypeName:

  def __init__(self, base, suffix):
    self.base = base
    self.suffix = suffix

  @property
  def compound(self):
    return self.base + self.suffix

  def __str__(self):
    return self.compound

class LibTypeInfo:

  def __init__(self, expr):
    self.expr = expr
    base, suffix = expr.build_desc()
    self.name = LibTypeName(base, suffix)

class TypeInfo:

  def __init__(
    self,
    jinjenv,
    lib_expr,
    kl_name_base=None,
    kl_name_suffix=None,
    edk_name=None,
    child_dqtis=[],
    extends=None,
    record=None,
    is_simple=False,
    ):
    if kl_name_base is not None:
      if not kl_name_suffix:
        kl_name_suffix = ''
      self.kl = KLTypeInfo(kl_name_base, kl_name_suffix)
      if not edk_name:
        assert not kl_name_suffix
        edk_name = "_Kludge_EDK_" + kl_name_base
    if edk_name:
      self.edk = EDKTypeInfo(edk_name)
    self.lib = LibTypeInfo(lib_expr)
    self.jinjenv = jinjenv
    self.child_dqtis = child_dqtis
    assert extends is None or isinstance(extends, TypeInfo)
    self.extends = extends
    assert record is None or isinstance(record, Record)
    self.record = record
    self.is_simple = is_simple
    self._codec_lookup_rules = None

  def get_desc(self):
    return "KL[%s] EDK[%s] LIB[%s]" % (self.kl.name, self.edk.name, self.lib.name)
  
  def __str__(self):
    return self.get_desc()

  def build_codec_lookup_rules(self):
    return {
      "conv": {"*": "protocols/conv/builtin/default"},
      "result": {"*": "protocols/result/builtin/indirect"},
      "param": {"*": "protocols/param/builtin/default"},
      "self": {"*": "protocols/self/builtin/default"},
      "repr": {"*": "protocols/repr/builtin/in_place"},
      }

  def _resolve_proto_dir(self, proto, obj):
    if not self._codec_lookup_rules:
      self._codec_lookup_rules = self.build_codec_lookup_rules()
    proto_dict = self._codec_lookup_rules.get(proto)
    if proto_dict:
      obj_dir = proto_dict.get(obj)
      if obj_dir:
        return obj_dir
      default_obj_dir = proto_dict.get("*")
      if default_obj_dir:
        return default_obj_dir
    raise Exception("Unable to resolve proto='%s', obj='%s' in codec_lookup_rules = '%s'" % (proto, obj, str(self._codec_lookup_rules)))

  def _render(self, proto, obj, lang, env):
    template_path = "%s/%s.%s" % (self._resolve_proto_dir(proto, obj), obj, lang)
    # print "template_path = " + template_path
    content = self.jinjenv.get_template(template_path).render(env).strip()
    if self.jinjenv.opts.debug_templates and content:
      content = "/*%s:BEGIN*/%s/*%s:END*/" % (template_path, content, template_path)
    return content

  def render_get_underlying_ptr(self, expr):
    return self._render("repr", "get_underlying_ptr", "kl", {
      "type_info": self,
      "expr": expr,
      })
