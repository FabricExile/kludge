#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import os, sys, optparse, re, traceback, StringIO
import clang
from clang.cindex import AccessSpecifier, CursorKind, TypeKind
from libkludge import util
from libkludge.member_access import MemberAccess

class Parser(object):

  def __init__(self, name, opts):
    self.name = name
    self.opts = opts
    self.clang_opts = ['-x', 'c++']
    if self.opts.clang_opts:
      self.clang_opts.extend(self.opts.clang_opts)
    if self.opts.cpppath:
      for cppdir in self.opts.cpppath:
          self.clang_opts.extend(["-I", self.expand_envvars(cppdir)])
    self.clang_opts.extend(["-isystem", self.expand_envvars('${KLUDGE_LLVM_ROOT}/include/c++/v1')])
    self.clang_opts.extend(["-isystem", self.expand_envvars('${KLUDGE_LLVM_ROOT}/lib/clang/3.9.0/include')])
    if self.opts.cppdefines:
      for cppdefine in self.opts.cppdefines:
          self.clang_opts.extend(["-D", self.expand_envvars(cppdefine)])
    self.info("Using Clang options: %s" % " ".join(self.clang_opts))

  def error(self, string):
    util.error(self.opts, string)

  def warning(self, string):
    util.warning(self.opts, string)

  def info(self, string):
    util.info(self.opts, string)

  def debug(self, string):
    util.debug(self.opts, string)

  @staticmethod
  def location_desc(location):
    return "%s:%d:%d" % (location.file, location.line, location.column)

  class ASTLogger(object):

    def __init__(self, parser, prefix="AST:"):
      self.parser = parser
      self.prefix = prefix

    def log_cursor(self, cursor):
      self.parser.debug("%s %s %s %s" % (self.prefix, str(cursor.kind), cursor.displayname, self.parser.location_desc(cursor.location)))

    def log_children(self, cursor):
      child_ast_logger = self.indent()
      for child_cursor in cursor.get_children():
        child_ast_logger.log_cursor(child_cursor)
        child_ast_logger.log_children(child_cursor)

    def indent(self):
      return self.parser.ASTLogger(self.parser, self.prefix + ":")

  envvar_re = re.compile("\\${[A-Za-z_]+}")

  @classmethod
  def expand_envvars(cls, string_value):
    while True:
        match_object = cls.envvar_re.match(string_value)
        if not match_object:
            break
        try:
            envvar_name = string_value[match_object.start(0)+2:match_object.end(0)-1]
            envvar_value = os.environ[envvar_name]
        except Exception, e:
            raise Exception("Missing environment variable " + envvar_name)
        string_value = \
              string_value[:match_object.start(0)] \
            + envvar_value \
            + string_value[match_object.end(0):]
    return string_value

  @classmethod
  def escape_cxxflag(cls, string_value):
      return string_value.replace('"', '\\\\"')

  def process(self, filename):
    self.parse(self.expand_envvars(filename))

  ignored_cursor_kinds = [
      CursorKind.MACRO_DEFINITION,
      CursorKind.INCLUSION_DIRECTIVE,
      ]

  def parse_params(
    self,
    ast_logger,
    cursor,
    ):
    params = []
    child_ast_logger = ast_logger.indent()
    for child_cursor in cursor.get_children():
      child_ast_logger.log_cursor(child_cursor)
      if child_cursor.kind == CursorKind.PARM_DECL:
        params.append(child_cursor.type.spelling)
      elif child_cursor.kind == CursorKind.TYPE_REF:
        pass
      elif child_cursor.kind == CursorKind.NAMESPACE_REF:
        pass
      elif child_cursor.kind == CursorKind.TEMPLATE_REF:
        pass
      else:
        self.warning("%s: Unhandled %s" % (self.location_desc(child_cursor.location), child_cursor.kind))
    return "[%s]" % (', '.join(["'%s'" % param for param in params]))

  def parse_comment(
    self,
    ast_logger,
    cursor,
    ):
    if cursor.raw_comment:
      return '.add_comment("""%s""")' % cursor.raw_comment
    else:
      return ''

  access_specifier_descs = {
    AccessSpecifier.PRIVATE: 'MemberAccess.private',
    AccessSpecifier.PROTECTED: 'MemberAccess.protected',
    AccessSpecifier.PUBLIC: 'MemberAccess.public',
    }

  def parse_method_access(
    self,
    ast_logger,
    cursor,
    ):
    if cursor.is_const_method():
      return "access=ThisAccess.const"
    elif cursor.is_static_method():
      return "access=ThisAccess.static"
    else:
      return "access=ThisAccess.mutable"

  def parse_record_decl(
    self,
    ast_logger,
    cursor,
    decls,
    defns,
    ):
    name = cursor.type.spelling
    extends = None
    members = []
    methods = []

    has_child = False
    child_ast_logger = ast_logger.indent()
    for child_cursor in cursor.get_children():
      has_child = True
      child_ast_logger.log_cursor(child_cursor)
      if child_cursor.kind == CursorKind.CXX_BASE_SPECIFIER:
        if extends:
          self.warning("%s: Unable to handle multiple base classes" % self.location_desc(child_cursor.location))
        extends = child_cursor.type.spelling
      elif child_cursor.kind == CursorKind.CXX_ACCESS_SPEC_DECL:
        pass
      elif child_cursor.kind == CursorKind.FIELD_DECL:
        members.append(
          "ty_%s.add_member('%s', '%s', access=%s)\n" % (
            name,
            child_cursor.spelling,
            child_cursor.type.spelling,
            self.access_specifier_descs[child_cursor.access_specifier],
            )
          )
      elif child_cursor.kind == CursorKind.CONSTRUCTOR:
        if child_cursor.access_specifier == AccessSpecifier.PUBLIC:
          methods.append(
            "ty_%s.add_ctor(%s)\n" % (
              name,
              self.parse_params(child_ast_logger, child_cursor)
              )
            )
      elif child_cursor.kind == CursorKind.CONVERSION_FUNCTION:
        if child_cursor.access_specifier == AccessSpecifier.PUBLIC:
          methods.append(
            "ty_%s.add_cast('%s')\n" % (
              name,
              child_cursor.result_type.spelling
              )
            )
      elif child_cursor.kind == CursorKind.CXX_METHOD:
        if child_cursor.access_specifier == AccessSpecifier.PUBLIC:
          if child_cursor.spelling == "operator=":
            pass
          elif child_cursor.spelling == "operator++":
            methods.append(
              "ty_%s.add_uni_op('++', 'inc', '%s')\n" % (
                name,
                child_cursor.result_type.spelling,
                )
              )
          elif child_cursor.spelling == "operator--":
            methods.append(
              "ty_%s.add_uni_op('--', 'dec', '%s')\n" % (
                name,
                child_cursor.result_type.spelling,
                )
              )
          elif child_cursor.spelling == "operator*":
            methods.append(
              "ty_%s.add_deref('deref', '%s', %s)\n" % (
                name,
                child_cursor.result_type.spelling,
                self.parse_method_access(child_ast_logger, child_cursor),
                )
              )
          else:
            methods.append(
              "ty_%s.add_method('%s', '%s', %s, %s)%s\n" % (
                name,
                child_cursor.spelling,
                child_cursor.result_type.spelling,
                self.parse_params(child_ast_logger, child_cursor),
                self.parse_method_access(child_ast_logger, child_cursor),
                self.parse_comment(child_ast_logger, child_cursor),
                )
              )
      elif child_cursor.kind == CursorKind.DESTRUCTOR:
        pass
      else:
        self.warning("%s: Unhandled %s" % (self.location_desc(child_cursor.location), child_cursor.kind))

    if has_child:
      decls.write("ty_%s = ext.add_direct_type('%s'" % (name, name))
      if extends:
        decls.write(", extends='%s'" % extends)
      decls.write(")%s\n" % self.parse_comment(ast_logger, cursor))
      for member in members:
        defns.write(member)
      for method in methods:
        defns.write(method)
      defns.write("\n")

  def parse_function_decl(self, ast_logger, cursor, decls, defns):
    defns.write("ext.add_func('%s', '%s', %s)%s\n\n" % (
      cursor.spelling,
      cursor.result_type.spelling,
      self.parse_params(ast_logger, cursor),
      self.parse_comment(ast_logger, cursor),
      ))

  def parse_cursor(self, ast_logger, cursor, decls, defns):
    ast_logger.log_cursor(cursor)
    if cursor.kind in Parser.ignored_cursor_kinds:
      pass
    elif cursor.kind == CursorKind.CLASS_DECL or cursor.kind == CursorKind.STRUCT_DECL:
      self.parse_record_decl(ast_logger, cursor, decls, defns)
    elif cursor.kind == CursorKind.FUNCTION_DECL:
      self.parse_function_decl(ast_logger, cursor, decls, defns)
    else:
      self.warning("%s: Unhandled %s" % (self.location_desc(cursor.location), cursor.kind))

  clang_diag_desc = {
    clang.cindex.Diagnostic.Fatal: "fatal",
    clang.cindex.Diagnostic.Error: "error",
    clang.cindex.Diagnostic.Warning: "warning",
    clang.cindex.Diagnostic.Note: "note",
    }

  def parse(self, filename):
    ast_logger = self.ASTLogger(self)

    self.info("Parsing '%s'" % filename)

    clang_index = clang.cindex.Index.create()
    unit = clang_index.parse(
        filename,
        self.clang_opts,
        None,
        clang.cindex.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES,
        # clang.cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD
        )

    displayed_separator = False
    fatal_error_count = 0
    for diag in unit.diagnostics:
      if not displayed_separator:
        print "-" * 78
        displayed_separator = True
      prefix = "%s:%d:%d: %s: " % (diag.location.file, diag.location.line, diag.location.column, self.clang_diag_desc[diag.severity])
      self.info(prefix + diag.spelling)
      space_prefix = ' ' * len(prefix)
      for fixit in diag.fixits:
        self.info(space_prefix + str(fixit))
      if diag.severity >= clang.cindex.Diagnostic.Fatal:
        fatal_error_count += 1
    if displayed_separator:
      print "-" * 78
    if fatal_error_count > 0:
        self.error("Fatal compile errors encountered; aborting")
        return 0

    decls = StringIO.StringIO()
    defns = StringIO.StringIO()
    for cursor in unit.cursor.get_children():
        if hasattr(cursor.location.file, 'name') \
          and cursor.location.file.name != filename:
          continue
        self.parse_cursor(ast_logger, cursor, decls, defns)
    print "-" * 78
    print decls.getvalue()
    print defns.getvalue()
