#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

import os, abc, jinja2

class Decl(object):
  def __init__(
    self,
    parent_namespace,
    is_kludge_ext=False,
    ):
    self.parent_namespace = parent_namespace
    self.is_kludge_ext = is_kludge_ext

    for method_name in [
      'error',
      'warning',
      'info',
      'debug',
      ]:
      setattr(self, method_name, getattr(parent_namespace, method_name))

  @property
  def ext(self):
    return self.parent_namespace.ext

  @property
  def cpp_type_expr_parser(self):
    return self.parent_namespace.cpp_type_expr_parser

  @property
  def type_mgr(self):
    return self.parent_namespace.type_mgr

  @property
  def namespace_mgr(self):
    return self.parent_namespace.namespace_mgr

  def add_test(self, kl, out, skip_epilog=False):
    self.ext.add_test(
      kl,
      out,
      test_name=self.get_test_name(),
      skip_epilog=skip_epilog,
      )
    return self

  @abc.abstractmethod
  def get_desc(self):
    pass

  @abc.abstractmethod
  def get_test_name(self):
    pass

  @abc.abstractmethod
  def get_template_path(self):
    pass

  def get_template_aliases(self):
    return []

  def render(self, context, lang, extras={}):
    path = self.get_template_path()
    template_vars = {'decl': self}
    for template_alias in self.get_template_aliases():
      template_vars.setdefault(template_alias, self)
    for k, v in extras.iteritems():
      template_vars.setdefault(k, v)
    try:
      template_path = path+'.'+context+'.'+lang
      template = self.ext.jinjenv.get_template(template_path)
    except jinja2.TemplateNotFound:
      template = None
    if template:
      return template.render(template_vars)
    else:
      return ''
