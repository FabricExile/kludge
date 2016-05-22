#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from symbol_helpers import replace_invalid_chars

class KLTypeName:

  def __init__(self, base, suffix):
    self.base = base
    self.suffix = suffix

  @property
  def compound(self):
    return self.base + self.suffix

class KLTypeInfo:

  def __init__(self, name_base, name_suffix):
    self.name = KLTypeName(name_base, name_suffix)

class EDKTypeName:

  def __init__(self, toplevel, local):
    self.toplevel = toplevel
    self.local = local

class EDKTypeInfo:

  def __init__(self, name_toplevel, name_local):
    self.name = EDKTypeName(name_toplevel, name_local)

class LibTypeName:

  def __init__(self, base, suffix):
    self.base = base
    self.suffix = suffix

  @property
  def compound(self):
    return self.base + self.suffix
  

class LibTypeInfo:

  def __init__(self, expr):
    print "LibTypeInfo " + str(expr)
    self.expr = expr
    base, suffix = expr.build_desc()
    self.name = LibTypeName(base, suffix)

class TypeInfo:

  can_in_place = False

  def __init__(
    self,
    jinjenv,
    lib_expr,
    nested_name = None,
    edk_name_toplevel = None,
    edk_name_local = None,
    kl_name_base = None,
    kl_name_suffix = None,
    child_dqtis = [],
    ):
    if kl_name_base:
      self.kl = KLTypeInfo(kl_name_base, kl_name_suffix)
    else:
      kl_name = "_".join(nested_name)
      kl_name = replace_invalid_chars(kl_name)
      self.kl = KLTypeInfo(kl_name, "")
    if edk_name_toplevel:
      self.edk = EDKTypeInfo(edk_name_toplevel, edk_name_local)
    else:
      edk_name = "_".join(nested_name)
      edk_name = replace_invalid_chars(edk_name)
      self.edk = EDKTypeInfo("::Fabric::EDK::KL::" + edk_name, edk_name)
    self.lib = LibTypeInfo(lib_expr)
    self.jinjenv = jinjenv
    self.child_dqtis = child_dqtis
    self._codec_lookup_rules = None

  def get_desc(self):
    return self.kl.name.compound
    
  def build_codec_lookup_rules(self):
    return {
      "conv": {"*": "protocols/conv/builtin/default"},
      "result": {"*": "protocols/result/builtin/indirect"},
      "param": {"*": "protocols/param/builtin/default"},
      "self": {"*": "protocols/self/builtin/default"},
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
    if content:
      content = "// %s\n%s" % (template_path, content)
    return content

