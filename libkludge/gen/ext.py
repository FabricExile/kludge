#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import os, jinja2
from libkludge.namespace_mgr import NamespaceMgr
from libkludge.type_mgr import TypeMgr
from libkludge.ast.decl_set import DeclSet
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
      loader=jinja2.PrefixLoader({
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

    self.cpp_global_includes = []
    self.edk_decls = DeclSet()

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
      except Exception as e:
        raise Exception("Caught exception processing %s: %s" % (filename, e))

  def jinja_stream(self, lang):
      return self.jinjenv.get_template("gen/ext/ext.template." + lang).stream(
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
