#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

class TypeCodec:

  is_in_place = False

  def __init__(
    self,
    jinjenv,
    type_info,
    child_dqtcs = [],
    ):
    self.jinjenv = jinjenv
    self.type_info = type_info
    self.child_dqtcs = child_dqtcs
    self._type_dir_spec = None

  def build_type_dir_spec(self):
    return {
      "conv": {"*": "protocols/conv/builtin/default"},
      "result": {"*": "protocols/result/builtin/indirect"},
      "param": {"*": "protocols/param/builtin/default"},
      "self": {"*": "protocols/self/builtin/default"},
      }

  def _resolve_proto_dir(self, proto, obj):
    if not self._type_dir_spec:
      self._type_dir_spec = self.build_type_dir_spec()
    proto_dict = self._type_dir_spec.get(proto)
    if proto_dict:
      obj_dir = proto_dict.get(obj)
      if obj_dir:
        return obj_dir
      default_obj_dir = proto_dict.get("*")
      if default_obj_dir:
        return default_obj_dir
    raise Exception("Unable to resolve proto='%s', obj='%s' in type_dir_spec = '%s'" % (proto, obj, str(self._type_dir_spec)))

  def _render(self, proto, obj, lang, env):
    template_path = "%s/%s.%s" % (self._resolve_proto_dir(proto, obj), obj, lang)
    # print "template_path = " + template_path
    content = self.jinjenv.get_template(template_path).render(env).strip()
    if content:
      content = "// %s\n%s" % (template_path, content)
    return content
