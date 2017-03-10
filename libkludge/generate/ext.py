#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

import os, jinja2, inspect
from libkludge.namespace_mgr import NamespaceMgr
from libkludge.type_mgr import TypeMgr
from namespace import Namespace
from libkludge.visibility import Visibility
from this_access import ThisAccess
from param import Param
from test import Test
from libkludge import util
from libkludge.cpp_type_expr_parser import *

class CPPVerbatim:
  def __init__(self, text):
    self.text = text
  def render(self):
    return self.text

class Ext:

  def __init__(
    self,
    name,
    opts,
    ):
    self.name = name
    self.opts = opts

    self.jinjenv = jinja2.Environment(
      trim_blocks = True,
      lstrip_blocks = True,
      undefined = jinja2.StrictUndefined,
      loader = jinja2.PrefixLoader({
          "protocols": jinja2.PrefixLoader({
              "conv": jinja2.PrefixLoader({
                  "builtin": jinja2.PackageLoader('libkludge', 'protocols/conv'),
                  }),
              "result": jinja2.PrefixLoader({
                  "builtin": jinja2.PackageLoader('libkludge', 'protocols/result'),
                  }),
              "param": jinja2.PrefixLoader({
                  "builtin": jinja2.PackageLoader('libkludge', 'protocols/param'),
                  }),
              "self": jinja2.PrefixLoader({
                  "builtin": jinja2.PackageLoader('libkludge', 'protocols/self'),
                  }),
              "repr": jinja2.PrefixLoader({
                  "builtin": jinja2.PackageLoader('libkludge', 'protocols/repr'),
                  }),
              }),
          "types": jinja2.PrefixLoader({
              "builtin": jinja2.PackageLoader('libkludge', 'types'),
              }),
          "generate": jinja2.PackageLoader('libkludge', 'generate/templates'),
          }),
      )
    setattr(self.jinjenv, 'opts', opts)
    self.type_mgr = TypeMgr(self)
    self.namespace_mgr = NamespaceMgr(self.type_mgr)

    self.cpp_flags = []
    self.linker_flags = []
    self.cpp_defines = []
    self.cpp_include_dirs = []
    self.cpp_includes = []
    self.cpp_source_files = []
    self.cpp_topmosts = []
    self.cpp_prologs = []
    self.cpp_epilogs = []
    self.exception_prolog = None
    self.exception_epilog = None
    self.lib_dirs = []
    self.libs = []
    self.kl_requires = []
    self.kl_prologs = []
    self.kl_epilogs = []
    self.dfg_preset_dir = None
    self.dfg_preset_path = None
    self.decls = []
    self.tests = []
    self.cpp_type_expr_to_record = {}
    self.func_promotions = {}

    self.root_namespace = Namespace(self, None, [], None)
    for root_namespace_method in inspect.getmembers(
      self.root_namespace,
      predicate = inspect.ismethod,
      ):
      setattr(self, root_namespace_method[0], root_namespace_method[1])

    tys = [
      'bool',
      'char',
      'int8_t',
      'unsigned char',
      'uint8_t',
      'short',
      'int16_t',
      'unsigned short',
      'uint16_t',
      'int',
      'int32_t',
      'unsigned',
      'uint32_t',
      'long long',
      'int64_t',
      'unsigned long long',
      'uint64_t',
      'size_t',
      'ptrdiff_t',
      'intptr_t',
      'float',
      'double',
      'std::string',
      'char const *',
      ]

    tys_d = []
    for ty in tys:
      tys_d.append(ty)
      tys_d.append('std::vector< ' + ty + ' >')

    tys_d_d = []
    for ty in tys_d:
      tys_d_d.append(ty)
      tys_d_d.append(ty + ' *')
      tys_d_d.append(ty + ' &')
      tys_d_d.append(ty + ' const *')
      tys_d_d.append(ty + ' const &')

    cpp_type_expr_parser = self.cpp_type_expr_parser
    self.kludge_ext_cpp_type_exprs = []
    for ty in tys_d_d:
      self.kludge_ext_cpp_type_exprs.append(cpp_type_expr_parser.parse(ty))

  def is_kludge_ext_cpp_type_expr(self, cpp_type_expr):
    result = cpp_type_expr in self.kludge_ext_cpp_type_exprs
    # print "is_kludge_ext_cpp_type_expr(" + str(cpp_type_expr) + ") = " + str(result)
    return result

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

  def process_glbls(self):
    glbls = {
      'ext': self,
      'Param': Param,
      'ThisAccess': ThisAccess,
      'Visibility': Visibility,
      }
    def process(filename, file_or_string):
      self.info("Processing %s" % filename)
      try:
        exec file_or_string in glbls
      except:
        self.error("Caught exception processing %s:" % filename)
        raise
    glbls['process'] = process
    def include(filename):
      with open(filename, "r") as file:
        process(filename, file)
    glbls['include'] = include
    return glbls

  def process(self, filename, file_or_string_or_none=None):
    glbls = self.process_glbls()
    if file_or_string_or_none:
      glbls['process'](filename, file_or_string_or_none)
    else:
      glbls['include'](filename)

  def add_decl(self, decl):
    self.decls.append(decl)

  def add_test(self, kl, out, test_name=None, skip_epilog=False):
    if not test_name:
      test_name = "TEST_%d" % len(self.tests)
    self.tests.append(Test(
      test_name,
      self.jinjenv,
      kl,
      out,
      skip_epilog=skip_epilog,
      ))

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
        self.jinjenv.get_template("generate/ext/ext." + lang).stream(ext=self).dump(file)

  def add_cpp_flag(self, cpp_flag):
    self.cpp_flags.append(os.path.expandvars(cpp_flag))

  def add_linker_flag(self, linker_flag):
    self.linker_flags.append(os.path.expandvars(linker_flag))

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

  def add_cpp_source_file(self, filepath):
    self.debug("Extension: Adding C++ source file '%s'" % filepath)
    self.cpp_source_files.append(filepath)
  
  def add_cpp_topmost(self, cpp_topmost):
    self.cpp_topmosts.append(CPPVerbatim(cpp_topmost))

  def add_cpp_prolog(self, cpp_prolog):
    self.cpp_prologs.append(CPPVerbatim(cpp_prolog))
  
  def add_cpp_epilog(self, cpp_epilog):
    self.cpp_epilogs.append(CPPVerbatim(cpp_epilog))
  
  def add_kl_prolog(self, kl_prolog):
    self.kl_prologs.append(kl_prolog)
  
  def add_kl_epilog(self, kl_epilog):
    self.kl_epilogs.append(kl_epilog)

  def set_cpp_exception_prolog(self, exception_prolog):
    self.exception_prolog = exception_prolog

  def set_cpp_exception_epilog(self, exception_epilog):
    self.exception_epilog = exception_epilog

  def add_lib_dir(self, lib_dir):
    self.lib_dirs.append(os.path.expandvars(lib_dir))

  def add_lib(self, lib):
    self.libs.append(os.path.expandvars(lib))

  def add_kl_require(self, kl_ext_name):
    self.debug("Extension: Adding KL require '%s'" % kl_ext_name)
    self.kl_requires.append(kl_ext_name)

  def add_dfg_presets_spec(self, preset_path, dir_="DFG"):
    self.debug("Extension: Adding DFG presets spec %s:%s/" % (preset_path, dir_))
    self.dfg_preset_path = preset_path
    self.dfg_preset_dir = dir_

  def instantiate_cpp_type_expr(self, cpp_type_expr):
    self.type_mgr.get_dqti(cpp_type_expr)
