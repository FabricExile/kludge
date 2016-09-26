#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import os, sys, optparse, re, traceback, StringIO, tempfile
import clang
from clang.cindex import AccessSpecifier, CursorKind, TypeKind
from libkludge import util
from libkludge.member_access import MemberAccess

class Parser(object):

  def __init__(self, name, opts):
    self.name = name
    self.opts = opts
    self.opts.dirs_to_ignore = [self.expand_envvars(dir) for dir in self.opts.dirs_to_ignore]
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

  ignored_cursor_kinds = [
      CursorKind.MACRO_DEFINITION,
      CursorKind.INCLUSION_DIRECTIVE,
      ]

  def param_count(self, cursor):
    result = 0
    for child_cursor in cursor.get_children():
      if child_cursor.kind == CursorKind.PARM_DECL:
        result += 1
    return result

  def parse_params(
    self,
    ast_logger,
    cursor,
    ):
    params = []
    opt_params = []
    child_ast_logger = ast_logger.indent()
    for child_cursor in cursor.get_children():
      child_ast_logger.log_cursor(child_cursor)
      if child_cursor.kind == CursorKind.PARM_DECL:
        has_grandchild = False
        grandchild_ast_logger = child_ast_logger.indent()
        for grandchild_cursor in child_cursor.get_children():
          grandchild_ast_logger.log_cursor(grandchild_cursor)
          if grandchild_cursor.kind == CursorKind.DECL_REF_EXPR:
            has_grandchild = True
            break
        if has_grandchild:
          opt_params.append((child_cursor.spelling, child_cursor.type.spelling))
        else:
          params.append((child_cursor.spelling, child_cursor.type.spelling))          
      elif child_cursor.kind == CursorKind.TYPE_REF:
        pass
      elif child_cursor.kind == CursorKind.NAMESPACE_REF:
        pass
      elif child_cursor.kind == CursorKind.TEMPLATE_REF:
        pass
      else:
        self.warning("%s: Unhandled %s" % (self.location_desc(child_cursor.location), child_cursor.kind))
    result = "[%s]" % (', '.join(["Param('%s', '%s')" % param for param in params]))
    if len(opt_params) > 0:
      result = "%s, [%s]" % (result, ', '.join(["Param('%s', '%s')" % opt_param for opt_param in opt_params]))
    return result

  def parse_comment(
    self,
    ast_logger,
    cursor,
    ):
    if cursor.raw_comment:
      comment = cursor.raw_comment
      comment = comment.replace('\\', '\\\\')
      comment = comment.replace('"', '\\"')
      return '\\\n  .add_comment("""%s""")' % comment
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
      return "this_access=ThisAccess.const"
    elif cursor.is_static_method():
      return "this_access=ThisAccess.static"
    else:
      return "this_access=ThisAccess.mutable"

  def parse_record_decl(
    self,
    ast_logger,
    cursor,
    obj,
    decls,
    defns,
    ):
    name = cursor.spelling
    child_obj = '%s_%s' % (obj, name)
    extends = None
    decl_warnings = []
    members = []
    methods = []
    child_record_cursors = []

    has_child = False
    child_ast_logger = ast_logger.indent()
    for child_cursor in cursor.get_children():
      has_child = True
      child_ast_logger.log_cursor(child_cursor)
      if child_cursor.kind == CursorKind.CXX_BASE_SPECIFIER:
        if extends:
          decl_warnings.append("# Kludge WARNING: %s: Unable to handle multiple base classes" % self.location_desc(child_cursor.location))
        extends = child_cursor.type.spelling
      elif child_cursor.kind == CursorKind.CXX_ACCESS_SPEC_DECL:
        pass
      elif child_cursor.kind == CursorKind.FIELD_DECL:
        members.append(
          "# %s\n%s.add_member('%s', '%s', access=%s)" % (
            self.location_desc(child_cursor.location),
            child_obj,
            child_cursor.spelling,
            child_cursor.type.spelling,
            self.access_specifier_descs[child_cursor.access_specifier],
            )
          )
      elif child_cursor.kind == CursorKind.CONSTRUCTOR:
        if child_cursor.access_specifier == AccessSpecifier.PUBLIC:
          methods.append(
            "# %s\n%s.add_ctor(%s)%s" % (
              self.location_desc(child_cursor.location),
              child_obj,
              self.parse_params(child_ast_logger, child_cursor),
              self.parse_comment(child_ast_logger, child_cursor),
              )
            )
      elif child_cursor.kind == CursorKind.CONVERSION_FUNCTION:
        if child_cursor.access_specifier == AccessSpecifier.PUBLIC:
          methods.append(
            "# %s\n%s.add_cast('%s')%s" % (
              self.location_desc(child_cursor.location),
              child_obj,
              child_cursor.result_type.spelling,
              self.parse_comment(child_ast_logger, child_cursor),
              )
            )
      elif child_cursor.kind == CursorKind.CXX_METHOD:
        if child_cursor.access_specifier == AccessSpecifier.PUBLIC:
          if child_cursor.spelling == "operator=":
            pass
          elif child_cursor.spelling == "operator++":
            methods.append(
              "# %s\n%s.add_uni_op('++', 'inc', '%s')%s" % (
                self.location_desc(child_cursor.location),
                child_obj,
                child_cursor.result_type.spelling,
                self.parse_comment(child_ast_logger, child_cursor),
                )
              )
          elif child_cursor.spelling == "operator--":
            methods.append(
              "# %s\n%s.add_uni_op('--', 'dec', '%s')%s" % (
                self.location_desc(child_cursor.location),
                child_obj,
                child_cursor.result_type.spelling,
                self.parse_comment(child_ast_logger, child_cursor),
                )
              )
          elif child_cursor.spelling == "operator*":
            if self.param_count(child_cursor) == 0:
              methods.append(
                "# %s\n%s.add_deref('deref', '%s', %s)" % (
                  self.location_desc(child_cursor.location),
                  child_obj,
                  child_cursor.result_type.spelling,
                  self.parse_method_access(child_ast_logger, child_cursor),
                  )
                )
            else:
              methods.append("# Kludge WARNING: %s: Unhandled %s" % (self.location_desc(child_cursor.location), child_cursor.kind))
          else:
            methods.append(
              "# %s\n%s.add_method('%s', '%s', %s, %s)%s" % (
                self.location_desc(child_cursor.location),
                child_obj,
                child_cursor.spelling,
                child_cursor.result_type.spelling,
                self.parse_params(child_ast_logger, child_cursor),
                self.parse_method_access(child_ast_logger, child_cursor),
                self.parse_comment(child_ast_logger, child_cursor),
                )
              )
      elif child_cursor.kind == CursorKind.DESTRUCTOR:
        pass
      elif child_cursor.kind == CursorKind.CLASS_DECL \
        or child_cursor.kind == CursorKind.STRUCT_DECL \
        or child_cursor.kind == CursorKind.ENUM_DECL \
        or child_cursor.kind == CursorKind.TYPEDEF_DECL:
        child_record_cursors.append(child_cursor)
      else:
        methods.append("# Kludge WARNING: %s: Unhandled %s" % (self.location_desc(child_cursor.location), child_cursor.kind))

    if has_child:
      for decl_warning in decl_warnings:
        print >>decls, decl_warning
      decls.write("# %s\n%s = %s.add_owned_type('%s'" % (
        self.location_desc(cursor.location),
        child_obj,
        obj,
        name,
        ))
      if extends:
        decls.write(", extends='%s'" % extends)
      decls.write(")%s\n" % self.parse_comment(ast_logger, cursor))
      for child_record_cursor in child_record_cursors:
        child_ast_logger.log_cursor(child_record_cursor)
        self.parse_cursor(child_ast_logger, child_record_cursor, child_obj, decls, defns)
      for member in members:
        print >>defns, member
      for method in methods:
        print >>defns, method
      print >>defns, ""

  def parse_function_decl(self, ast_logger, cursor, obj, decls, defns):
    defns.write("# %s\n%s.add_func('%s', '%s', %s)%s\n\n" % (
      self.location_desc(cursor.location),
      obj,
      cursor.spelling,
      cursor.result_type.spelling,
      self.parse_params(ast_logger, cursor),
      self.parse_comment(ast_logger, cursor),
      ))

  def parse_enum_decl(self, ast_logger, cursor, obj, decls, defns):
    values = []
    child_ast_logger = ast_logger.indent()
    for child_cursor in cursor.get_children():
      has_child = True
      child_ast_logger.log_cursor(child_cursor)
      if child_cursor.kind == CursorKind.ENUM_CONSTANT_DECL:
        values.append((child_cursor.spelling, child_cursor.enum_value))
      else:
        decls.write("# Kludge WARNING: %s: Unhandled %s\n" % (self.location_desc(child_cursor.location), child_cursor.kind))
    decls.write("# %s\n%s.add_enum('%s', [%s])%s\n" % (
      self.location_desc(cursor.location),
      obj,
      cursor.spelling,
      ', '.join(["('%s', %d)" % value for value in values]),
      self.parse_comment(ast_logger, cursor),
      ))

  def parse_typedef_decl(self, ast_logger, cursor, obj, decls, defns):
    decls.write("# %s\n%s.add_alias('%s', '%s')%s\n" % (
      self.location_desc(cursor.location),
      obj,
      cursor.spelling,
      cursor.underlying_typedef_type.spelling,
      self.parse_comment(ast_logger, cursor),
      ))

  def parse_namespace(self, ast_logger, cursor, obj, decls, defns):
    name = cursor.spelling
    child_obj = "%s_%s" % (obj, name)
    print >>decls, "# %s\n%s = %s.add_namespace('%s')" % (
      self.location_desc(cursor.location),
      child_obj,
      obj,
      name,
      )
    child_ast_logger = ast_logger.indent()
    for child_cursor in cursor.get_children():
      child_ast_logger.log_cursor(cursor)
      self.parse_cursor(child_ast_logger, child_cursor, child_obj, decls, defns)

  def parse_cursor(self, ast_logger, cursor, obj, decls, defns):
    if cursor.kind in Parser.ignored_cursor_kinds:
      pass
    elif cursor.kind == CursorKind.CLASS_DECL or cursor.kind == CursorKind.STRUCT_DECL:
      self.parse_record_decl(ast_logger, cursor, obj, decls, defns)
    elif cursor.kind == CursorKind.ENUM_DECL:
      self.parse_enum_decl(ast_logger, cursor, obj, decls, defns)
    elif cursor.kind == CursorKind.TYPEDEF_DECL:
      self.parse_typedef_decl(ast_logger, cursor, obj, decls, defns)
    elif cursor.kind == CursorKind.FUNCTION_DECL:
      self.parse_function_decl(ast_logger, cursor, obj, decls, defns)
    elif cursor.kind == CursorKind.NAMESPACE:
      self.parse_namespace(ast_logger, cursor, obj, decls, defns)
    else:
      print >>defns, "# Kludge WARNING: %s: Unhandled %s" % (self.location_desc(cursor.location), cursor.kind)

  clang_diag_desc = {
    clang.cindex.Diagnostic.Fatal: "fatal",
    clang.cindex.Diagnostic.Error: "error",
    clang.cindex.Diagnostic.Warning: "warning",
    clang.cindex.Diagnostic.Note: "note",
    }

  def should_ignore_dir(self, dirpath):
    for dir in self.opts.dirs_to_ignore:
      if dirpath.startswith(dir):
        return True
    return False

  def process(self, ext_name, dirs_and_files):
    ast_logger = self.ASTLogger(self)

    includes = []
    for dir_or_file in dirs_and_files:
      if os.path.isfile(dir_or_file):
        includes.append(self.expand_envvars(dir_or_file))
      elif os.path.isdir(dir_or_file):
        for dirpath, dirnames, filenames in os.walk(self.expand_envvars(dir_or_file)):
          if self.should_ignore_dir(dirpath):
            self.info("Ignoring directory '%s'" % dirpath)
            continue
          for filename in filenames:
            if filename.endswith('.h') or filename.endswith('.hpp') or filename.endswith('.hxx'):
              includes.append(os.path.join(dirpath, filename))
      else:
        self.error("'%s': not a file or directory" % dir_or_file)
        return 0

    self.info("Generated temporary inclusion header:")
    print "  +-" + ("-" * 78)
    for include in includes:
      print '  | #include "%s"' % include
    print "  +-" + ("-" * 78)

    include_abspaths = [os.path.abspath(include) for include in includes]

    with tempfile.NamedTemporaryFile(prefix='kludge_', suffix='.h', mode='w', dir=os.getcwd()) as includer:
      for include in includes:
        print >>includer, '#include "%s"' % include
      includer.flush()

      self.info("Parsing temporary inclusion header with Clang")

      clang_index = clang.cindex.Index.create()
      unit = clang_index.parse(
          includer.name,
          self.clang_opts,
          None,
          clang.cindex.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES,
          # clang.cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD
          )

      displayed_separator = False
      fatal_error_count = 0
      for diag in unit.diagnostics:
        if not displayed_separator:
          print "Clang diagnostics:"
          print "  +-" + ("-" * 78)
          displayed_separator = True
        prefix = "  | %s:%d:%d: %s: " % (diag.location.file, diag.location.line, diag.location.column, self.clang_diag_desc[diag.severity])
        self.info(prefix + diag.spelling)
        space_prefix = ' ' * len(prefix)
        for fixit in diag.fixits:
          self.info(space_prefix + str(fixit))
        if diag.severity >= clang.cindex.Diagnostic.Fatal:
          fatal_error_count += 1
      if displayed_separator:
        print "  +-" + ("-" * 78)
      if fatal_error_count > 0:
          self.error("Fatal compile errors encountered; aborting")
      else:
        basename = ext_name
        decls_basename = basename + '.decls.kludge.py'
        decls_filename = os.path.join(self.opts.outdir, decls_basename)
        defns_basename = basename + '.defns.kludge.py'
        defns_filename = os.path.join(self.opts.outdir, defns_basename)
        with open(decls_filename, "w") as decls:
          self.info("Writing declarations to '%s'" % decls_filename)
          print >>decls, "#" * 78
          print >>decls, "## Automatically generated by Kludge"
          print >>decls, "#" * 78
          print >>decls

          with open(defns_filename, "w") as defns:
            self.info("Writing definitions to '%s'" % defns_filename)
            print >>defns, "#" * 78
            print >>defns, "## Automatically generated by Kludge"
            print >>defns, "#" * 78
            print >>defns

            for cursor in unit.cursor.get_children():
                if hasattr(cursor.location.file, 'name') \
                  and cursor.location.file.name not in include_abspaths:
                  self.debug("Skipping AST nodes for '%s'" % cursor.location.file.name)
                  continue
                ast_logger.log_cursor(cursor)
                self.parse_cursor(ast_logger, cursor, 'ext', decls, defns)
        master_filename = os.path.join(self.opts.outdir, basename + '.kludge.py')
        if self.opts.skip_master:
          self.info("Skipping generation of master")
        else:
          self.info("Writing master to '%s'" % master_filename)
          with open(master_filename, "w") as master:
            print >>master, "#" * 78
            print >>master, "## Automatically generated by Kludge"
            print >>master, "#" * 78
            print >>master
            if self.opts.clang_opts:
              for clang_opt in self.opts.clang_opts:
                print >>master, "ext.add_cpp_flag('%s')" % clang_opt
            if self.opts.cppdefines:
              for cppdefine in self.opts.cppdefines:
                print >>master, "ext.add_cpp_define('%s')" % cppdefine
            if self.opts.cpppath:
              for cppdir in self.opts.cpppath:
                print >>master, "ext.add_cpp_include_dir('%s')" % cppdir
            if self.opts.libpath:
              for libdir in self.opts.libpath:
                print >>master, "ext.add_lib_dir('%s')" % libdir
            if self.opts.libs:
              for lib in self.opts.libs:
                print >>master, "ext.add_lib('%s')" % lib
            print >>master
            if len(includes) > 0:
              for include in includes:
                print >>master, "ext.add_cpp_angled_include('%s')" % include
              print >>master
            print >>master, "include('%s')" % decls_basename
            print >>master, "include('%s')" % defns_basename
