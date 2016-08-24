#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import os, jinja2
from libkludge.namespace_mgr import NamespaceMgr
from libkludge.type_mgr import TypeMgr
from libkludge.ast.decl_set import DeclSet
from func import Func

class Ext:

  def __init__(self, name, opts):
    self.name = name
    self.opts = opts

    self.jinjenv = jinja2.Environment(
      trim_blocks = True,
      lstrip_blocks = True,
      undefined = jinja2.StrictUndefined,
      loader = jinja2.PackageLoader('__main__', 'libkludge/gen/templates'),
      )
    self.namespace_mgr = NamespaceMgr()
    self.type_mgr = TypeMgr(self.jinjenv)

    self.cpp_global_includes = []
    self.edk_decls = DeclSet()

  def log(self, level, string):
    if self.opts.verbosity >= level:
      print string

  def error(self, string):
    self.log(0, "Error: %s" % string)

  def warning(self, string):
    self.log(1, "Warning: %s" % string)

  def info(self, string):
    self.log(2, string)

  def debug(self, string):
    self.log(3, "Debug: %s" % string)

  def process(self, filename):
    with open(filename, "r") as file:
      self.info("Processing %s" % filename)
      try:
        exec file in {'ext': self}
      except Exception as e:
        raise Exception("Caught exception processing %s: %s" % (filename, e))

  def jinja_stream(self, lang):
      return self.jinjenv.get_template("ext/ext.template." + lang).stream(
        name = self.name,
        cpp_global_includes = self.cpp_global_includes,
        gen_decl_streams = lambda: self.edk_decls.jinja_streams(self.jinjenv, lang),
        )

  def write(self):
    for lang in [
      'kl',
      'cpp',
      'fpm.json',
      'SConstruct',
      ]:
      filename = os.path.join(self.opts.outdir, self.name + '.' + lang)
      self.info("Writing %s" % (filename))
      with open(filename, 'w') as file:
        self.jinja_stream(lang).dump(file)

  def add_cpp_global_include(self, cpp_global_include):
    self.debug("Adding C++ global include '%s'" % cpp_global_include)
    self.cpp_global_includes.append(cpp_global_include)

  def add_func(self, name):
    func = Func(self, name)
    self.edk_decls.add(func)
    return func
