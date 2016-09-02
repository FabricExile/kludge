#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import os, jinja2
from libkludge.namespace_mgr import NamespaceMgr
from libkludge.type_mgr import TypeMgr
from libkludge.cpp_type_expr_parser import Named, Simple, Template
from record import Record
from alias import Alias
from func import Func
from test import Test
from this_access import ThisAccess
from member_access import MemberAccess
from libkludge.types import InPlaceSelector
from libkludge.types import KLExtTypeAliasSelector
from libkludge.types import DirectSelector
from libkludge.types import WrappedSelector
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
              "repr": jinja2.PrefixLoader({
                  "builtin": jinja2.PackageLoader('__main__', 'libkludge/protocols/repr'),
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

    self.cpp_flags = []
    self.cpp_defines = []
    self.cpp_include_dirs = []
    self.cpp_includes = []
    self.lib_dirs = []
    self.libs = []
    self.kl_requires = []
    self.decls = []
    self.tests = []
    self.cpp_type_name_to_record = {}

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
    glbls = {
      'ext': self,
      'ThisAccess': ThisAccess,
      'MemberAccess': MemberAccess,
      }
    def include(filename):
      with open(filename, "r") as file:
        self.info("Processing %s" % filename)
        try:
          exec file in glbls
        except:
          self.error("Caught exception processing %s:" % filename)
          raise
    glbls['include'] = include
    include(filename)

  def add_test(self, test_name, kl, out):
    self.tests.append(Test(test_name, self.jinjenv, kl, out))

  def write(self):
    for lang in [
      'kl',
      'cpp',
      'fpm.json',
      'SConstruct',
      'test.kl',
      'test.out',
      'test.py',
      ]:
      filename = os.path.join(self.opts.outdir, self.name + '.' + lang)
      self.info("Writing %s" % (filename))
      with open(filename, 'w') as file:
        self.jinjenv.get_template("gen/ext/ext." + lang).stream(ext=self).dump(file)

  def add_cpp_flag(self, cpp_flag):
    self.cpp_flags.append(os.path.expandvars(cpp_flag))

  def add_cpp_define(self, cpp_define):
    self.cpp_defines.append(os.path.expandvars(cpp_define))

  def add_cpp_include_dir(self, cpp_include_dir):
    self.cpp_include_dirs.append(os.path.expandvars(cpp_include_dir))

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

  def add_lib_dir(self, lib_dir):
    self.lib_dirs.append(os.path.expandvars(lib_dir))

  def add_lib(self, lib):
    self.libs.append(os.path.expandvars(lib))

  def add_kl_require(self, kl_ext_name):
    self.debug("Extension: Adding KL require '%s'" % kl_ext_name)
    self.kl_requires.append(kl_ext_name)

  def add_func(self, name, returns=None, params=[]):
    func = Func(self, name)
    if returns:
      func.returns(returns)
    for param in params:
      func.add_param(param)
    self.decls.append(func)
    return func

  def add_alias(self, new_cpp_type_name, old_cpp_type_name):
    new_cpp_type_expr = Named([Simple(new_cpp_type_name)])
    old_cpp_type_expr = self.namespace_mgr.resolve_cpp_type_expr([], old_cpp_type_name)
    self.type_mgr.add_alias(new_cpp_type_expr, old_cpp_type_expr)
    new_kl_type_name = new_cpp_type_name
    old_dqti = self.type_mgr.maybe_get_dqti(old_cpp_type_expr)
    alias = Alias(self, new_kl_type_name, old_dqti.type_info)
    self.decls.append(alias)
    return alias

  def maybe_generate_kl_type_name(self, kl_type_name, cpp_type_expr):
    if not kl_type_name:
      assert isinstance(cpp_type_expr, Named)
      if isinstance(cpp_type_expr.components[0], Simple):
        kl_type_name = cpp_type_expr.components[0].name
      elif isinstance(cpp_type_expr.components[0], Template) \
        and len(cpp_type_expr.components[0].params) == 1 \
        and isinstance(cpp_type_expr.components[0].params[0], Named) \
        and isinstance(cpp_type_expr.components[0].params[0].components[0], Simple):
        kl_type_name = cpp_type_expr.components[0].params[0].components[0].name
      else:
        raise Exception(str(cpp_type_expr) + ": unable to generate kl_type_name")
    return kl_type_name

  def add_in_place_type(
    self,
    cpp_type_name,
    kl_type_name = None,
    ):
    cpp_type_expr = self.cpp_type_expr_parser.parse(cpp_type_name)
    kl_type_name = self.maybe_generate_kl_type_name(kl_type_name, cpp_type_expr)
    self.type_mgr.add_selector(
      InPlaceSelector(
        self.jinjenv,
        kl_type_name,
        [cpp_type_name],
        cpp_type_expr,
        )
      )
    record = Record(
      self,
      "InPlaceType: %s -> %s" % (kl_type_name, str(cpp_type_expr)),
      kl_type_name,
      self.type_mgr.get_dqti(cpp_type_expr).type_info,
      )
    self.decls.append(record)
    self.cpp_type_name_to_record[cpp_type_name] = record
    return record

  def add_direct_type(
    self,
    cpp_type_name,
    kl_type_name = None,
    extends = None
    ):
    cpp_type_expr = self.cpp_type_expr_parser.parse(cpp_type_name)
    kl_type_name = self.maybe_generate_kl_type_name(kl_type_name, cpp_type_expr)
    if extends:
      extends = self.cpp_type_name_to_record[extends]
    self.type_mgr.add_selector(
      DirectSelector(
        self.jinjenv,
        kl_type_name,
        [cpp_type_name],
        cpp_type_expr,
        False, #is_abstract,
        False, #no_copy_constructor,
        )
      )
    record = Record(
      self,
      "DirectType: %s -> %s" % (kl_type_name, str(cpp_type_expr)),
      kl_type_name,
      self.type_mgr.get_dqti(cpp_type_expr).type_info,
      extends = extends
      )
    self.decls.append(record)
    self.cpp_type_name_to_record[cpp_type_name] = record
    return record

  def add_wrapped_type(
    self,
    cpp_type_name,
    kl_type_name = None,
    extends = None
    ):
    cpp_type_expr = self.cpp_type_expr_parser.parse(cpp_type_name)
    assert isinstance(cpp_type_expr, Named) \
      and len(cpp_type_expr.components) == 1 \
      and isinstance(cpp_type_expr.components[0], Template) \
      and len(cpp_type_expr.components[0].params) == 1 \
      and isinstance(cpp_type_expr.components[0].params[0], Named) \
      and len(cpp_type_expr.components[0].params[0].components) == 1 \
      and isinstance(cpp_type_expr.components[0].params[0].components[0], Simple)
    kl_type_name = self.maybe_generate_kl_type_name(kl_type_name, cpp_type_expr)
    if extends:
      extends = self.cpp_type_name_to_record[extends]
    self.type_mgr.add_selector(
      WrappedSelector(
        self.jinjenv,
        kl_type_name,
        [cpp_type_name],
        cpp_type_expr,
        False, #is_abstract,
        False, #no_copy_constructor,
        )
      )
    record = Record(
      self,
      "WrappedType: %s -> %s" % (kl_type_name, str(cpp_type_expr)),
      kl_type_name,
      self.type_mgr.get_dqti(cpp_type_expr).type_info,
      extends = extends
      )
    self.decls.append(record)
    self.cpp_type_name_to_record[cpp_type_name] = record
    return record

  def add_kl_ext_type_alias(
    self,
    cpp_type_name,
    kl_ext_name,
    kl_type_name,
    ):
    cpp_type_expr = Named([Simple(cpp_type_name)])
    self.add_kl_require(kl_ext_name)
    self.type_mgr.add_selector(
      KLExtTypeAliasSelector(
        self.jinjenv,
        [cpp_type_name],
        cpp_type_expr,
        kl_type_name,
        )
      )
    record = Record(
      self,
      "KLExtTypeAlias: %s -> %s[%s]" % (cpp_type_name, kl_ext_name, kl_type_name),
      kl_type_name,
      self.type_mgr.get_dqti(cpp_type_expr).type_info,
      include_empty_ctor = False,
      include_copy_ctor = False,
      include_simple_ass_op = False,
      include_getters_setters = False,
      include_dtor = False,
      )
    self.decls.append(record)
    self.cpp_type_name_to_record[cpp_type_name] = record
    return record
