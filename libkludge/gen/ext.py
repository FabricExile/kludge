#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import os, jinja2
from libkludge.namespace_mgr import NamespaceMgr
from libkludge.type_mgr import TypeMgr
from libkludge.cpp_type_expr_parser import Named
from alias import Alias
from func import Func
import util

class Ext:

  def __init__(self, name, opts):
    self.name = name
    self.opts = opts

    self.jinjenv = jinja2.Environment(
      trim_blocks = True,
      lstrip_blocks = True,
      undefined = jinja2.StrictUndefined,
      loader = jinja2.PrefixLoader({
          "protocols": jinja2.PrefixLoader({
              "conv": jinja2.PrefixLoader({
                  "builtin": jinja2.PackageLoader('__main__', 'libkludge/protocols/conv'),
                  }),
              "result": jinja2.PrefixLoader({
                  "builtin": jinja2.PackageLoader('__main__', 'libkludge/protocols/result'),
                  }),
              "param": jinja2.PrefixLoader({
                  "builtin": jinja2.PackageLoader('__main__', 'libkludge/protocols/param'),
                  }),
              "self": jinja2.PrefixLoader({
                  "builtin": jinja2.PackageLoader('__main__', 'libkludge/protocols/self'),
                  }),
              }),
          "types": jinja2.PrefixLoader({
              "builtin": jinja2.PackageLoader('__main__', 'libkludge/types'),
              }),
          "gen": jinja2.PackageLoader('__main__', 'libkludge/gen/templates'),
          }),
      )
    self.namespace_mgr = NamespaceMgr()
    self.type_mgr = TypeMgr(self.jinjenv)

    self.cpp_includes = []
    self.decls = []

  @property
  def cpp_type_expr_parser(self):
    return self.namespace_mgr.cpp_type_expr_parser
  
  def error(self, string):
    util.error(self.opts, string)

  def warning(self, string):
    util.warning(self.opts, string)

  def info(self, string):
    util.info(self.opts, string)

  def debug(self, string):
    util.debug(self.opts, string)

  def process(self, filename):
    with open(filename, "r") as file:
      self.info("Processing %s" % filename)
      try:
        exec file in {'ext': self}
      except:
        self.error("Caught exception processing %s:" % filename)
        raise

  def write(self):
    for lang in [
      'kl',
      'cpp',
      'fpm.json',
      'SConstruct',
      'test.kl',
      'test.out',
      ]:
      filename = os.path.join(self.opts.outdir, self.name + '.' + lang)
      self.info("Writing %s" % (filename))
      with open(filename, 'w') as file:
        self.jinjenv.get_template("gen/ext/ext." + lang).stream(ext=self).dump(file)

  class CPPInclude:

    def __init__(self, filepath, is_angled):
      self.filepath = filepath
      self.is_angled = is_angled

  def add_cpp_quoted_include(self, filepath):
    self.debug("Extension: Adding C++ quoted include '%s'" % filepath)
    self.cpp_includes.append(self.CPPInclude(filepath, is_angled=False))

  def add_cpp_angled_include(self, filepath):
    self.debug("Extension: Adding C++ angled include '%s'" % filepath)
    self.cpp_includes.append(self.CPPInclude(filepath, is_angled=True))

  def add_func(self, name):
    func = Func(self, name)
    self.decls.append(func)
    return func

  def add_alias(self, new_cpp_type_name, old_cpp_type_name):
    new_cpp_type_expr = Named([new_cpp_type_name])
    old_cpp_type_expr = self.namespace_mgr.resolve_cpp_type_expr([], old_cpp_type_name)
    self.type_mgr.add_alias(new_cpp_type_expr, old_cpp_type_expr)
    new_kl_type_name = new_cpp_type_name
    old_dqti = self.type_mgr.maybe_get_dqti(old_cpp_type_expr)
    alias = Alias(self, new_kl_type_name, old_dqti.type_info)
    self.decls.append(alias)
    return alias
