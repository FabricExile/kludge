import jinja2, os, sys, optparse, json

import clang
from clang.cindex import AccessSpecifier, CursorKind, TypeKind

from kl2edk import KLStruct, Method, KLParam, TypesManager

import ast
from type_mgr import TypeMgr
from value_name import ValueName
from member import Member
from instance_method import InstanceMethod
from types import InPlaceStructSelector, WrappedPtrSelector
from param_codec import ParamCodec
from config import *
import clang_helpers
from namespace_mgr import NamespaceMgr

class CPPType:
    def __init__(self, type_name, is_pointer, is_const):
        self.type_name = type_name
        self.is_pointer = is_pointer
        self.is_const = is_const


class CustomMapping:
    def __init__(self, cpp_type_name, is_pointer, kl_type_name):
        self.cpp_type_name = cpp_type_name
        self.is_pointer = is_pointer
        self.kl_type_name = kl_type_name


import abc


class KLTypeMapping:
    def __init__(self, kl_type_name, cpp_type_name):
        self.kl_type_name = kl_type_name
        self.cpp_type_name = cpp_type_name

class Parser:
    __metaclass__ = abc.ABCMeta

    basic_type_map = {
        TypeKind.INVALID: None,
        TypeKind.UNEXPOSED: None,
        TypeKind.VOID: None,
        TypeKind.BOOL: "Boolean",
        TypeKind.CHAR_U: "Byte",
        TypeKind.UCHAR: "Byte",
        TypeKind.CHAR16: "UInt16",
        TypeKind.CHAR32: "SInt32",
        TypeKind.USHORT: "UInt16",
        TypeKind.UINT: "UInt32",
        TypeKind.ULONG: "UInt32",
        TypeKind.ULONGLONG: "UInt64",
        TypeKind.UINT128: "UInt64",
        TypeKind.CHAR_S: "SInt8",
        TypeKind.SCHAR: "SInt8",
        TypeKind.WCHAR: "UInt16",
        TypeKind.SHORT: "SInt16",
        TypeKind.INT: "SInt32",
        TypeKind.LONG: "SInt32",
        TypeKind.LONGLONG: "SInt64",
        TypeKind.INT128: "SInt64",
        TypeKind.FLOAT: "Float32",
        TypeKind.DOUBLE: "Float64",
        TypeKind.LONGDOUBLE: "Float64",
        TypeKind.NULLPTR: None,
        TypeKind.OVERLOAD: None,
        TypeKind.DEPENDENT: None,
        TypeKind.OBJCID: None,
        TypeKind.OBJCCLASS: None,
        TypeKind.OBJCSEL: None,
        TypeKind.COMPLEX: None,
        TypeKind.POINTER: None,
        TypeKind.BLOCKPOINTER: None,
        TypeKind.LVALUEREFERENCE: None,
        TypeKind.RVALUEREFERENCE: None,
        TypeKind.RECORD: None,
        TypeKind.ENUM: None,
        TypeKind.TYPEDEF: None,
        TypeKind.OBJCINTERFACE: None,
        TypeKind.OBJCOBJECTPOINTER: None,
        TypeKind.FUNCTIONNOPROTO: None,
        TypeKind.FUNCTIONPROTO: None,
        TypeKind.CONSTANTARRAY: None,
        TypeKind.VECTOR: None,
        TypeKind.MEMBERPOINTER: None,
        TypeKind.INCOMPLETEARRAY: None,
    }

    def __init__(self):
        self.edk_decls = ast.DeclSet()

    def main(self):
        self.config = create_default_config()

        try:
            opt_parser = optparse.OptionParser(
                usage="""
%prog [options] <EXTNAME> [<input1.h> <input2.h> ...]
OR %prog -c <config file>""",
                description="KLUDGE: C++-to-KL wrap-o-matic",
                )
            opt_parser.add_option(
                '-c', '--config',
                action='store',
                default='',
                dest='config',
                metavar='CONFIG.json',
                help="load options from CONFIG.json in JSON format",
                )
            opt_parser.add_option(
                '-o', '--outdir',
                action='store',
                default=self.config['outdir'],
                dest='outdir',
                metavar='OUTDIR',
                help="output directory (defaults to %s)" % self.config['outdir'],
                )
            opt_parser.add_option(
                '-b', '--basename',
                action='store',
                default=self.config['basename'],
                dest='basename',
                metavar='BASENAME',
                help="output OUTDIR/BASENAME.{kl,cpp} (defaults to EXTNAME)",
                )
            opt_parser.add_option(
                '--clang_opt',
                action='append',
                dest='clang_opts',
                metavar='CLANGOPT',
                help="pass additional option to clang++ (can be used multiple times)",
                )
            (opts, args) = opt_parser.parse_args()
        except Exception as e:
            print "Error: %s" % str(e)
            print "Run '%s --help' for usage" % sys.argv[0]
            sys.exit(1)

        if opts.config:
            with open(opts.config) as fh:
                 self.config.update(json.load(fh))

        if len(args) > 0:
            self.config['extname'] = args[0]
            for i in range(1, len(args)):
                self.config['infiles'].append(args[i])

        if len(opts.basename) > 0:
            self.config['basename'] = opts.basename

        if opts.clang_opts:
            self.config["clang_opts"].extend(opts.clang_opts)

        if opts.outdir:
            self.config['outdir'] = opts.outdir

        if not self.config['extname']:
            print "Usage error: You must specify the extension name"
            print "Use --help for detailed usage information"
            return
        if not self.config['infiles']:
            print "Usage error: You must provide at least one input file"
            print "Use --help for detailed usage information"
            return
        if not 'basename' in self.config:
            self.config['basename'] = self.config['extname']

        print "Using configuration:"
        json.dump(
            self.config,
            sys.stdout,
            sort_keys=True,
            indent=2,
            separators=(',', ': '),
            )
        sys.stdout.write("\n")

        self.jinjenv = create_jinjenv(self.config)
        self.type_mgr = TypeMgr(self.jinjenv)
        self.namespace_mgr = NamespaceMgr()

        for infile in self.config['infiles']:
            self.parse(infile)

        self.output(
            os.path.join(self.config['outdir'], self.config['basename'] + '.kl'),
            os.path.join(self.config['outdir'], self.config['basename'] + '.cpp'),
            )
        with open(os.path.join(self.config['outdir'], 'SConstruct'), "w") as fh:
            fh.write("""
#
# Copyright 2010-2015 Fabric Software Inc. All rights reserved.
#

import os, sys

extname = '%s'
basename = '%s'

try:
  fabricPath = os.environ['FABRIC_DIR']
except:
  print "You must set FABRIC_DIR in your environment."
  print "Refer to README.txt for more information."
  sys.exit(1)
SConscript(os.path.join(fabricPath, 'Samples', 'EDK', 'SConscript'))
Import('fabricBuildEnv')

fabricBuildEnv.Append(CPPPATH = ["../.."])
fabricBuildEnv.Append(CXXFLAGS = ["-g"])

fabricBuildEnv.SharedLibrary(
  '-'.join([extname, fabricBuildEnv['FABRIC_BUILD_OS'], fabricBuildEnv['FABRIC_BUILD_ARCH']]),
  [basename + '.cpp']
  )
""" % (self.config['extname'], self.config['basename']))
        with open(os.path.join(opts.outdir, self.config['extname']+'.fpm.json'), "w") as fh:
            fh.write("""
{
"libs": "%s",
"code": [
"actual.kl"
],
}
""" % self.config['extname'])

    # def get_kl_type(self, clang_type):
    #     canon_type = clang_type.get_canonical()
    #     base_name = canon_type.spelling
    #     if canon_type.is_const_qualified():
    #         base_name = base_name[len('const '):]
    #     kl_type = None
    #     is_array = False

    #     if canon_type.kind == TypeKind.LVALUEREFERENCE:
    #         kl_type = self.get_kl_type(canon_type.get_pointee())

    #     elif canon_type.kind == TypeKind.POINTER:
    #         if canon_type.get_pointee().kind == TypeKind.VOID:
    #             return "Data"
    #         if canon_type.get_pointee().kind in [TypeKind.CHAR_S,
    #                                              TypeKind.SCHAR]:
    #             return "String"
    #         kl_type = self.get_kl_type(canon_type.get_pointee())

    #     elif canon_type.kind == TypeKind.UNEXPOSED or canon_type.kind == TypeKind.RECORD:
    #         kl_type = base_name
    #         if kl_type.startswith('std::vector<'):
    #             is_array = True
    #             kl_type = kl_type[len('std::vector<'):kl_type.find(',')]
    #         if kl_type in self.cpp_type_to_kl_mappings:
    #             kl_type = self.cpp_type_to_kl_mappings[kl_type]

    #     elif canon_type.kind == TypeKind.TYPEDEF:
    #         kl_type = self.get_kl_type(canon_type.get_canonical())

    #     elif canon_type.kind == TypeKind.VOID:
    #         return None

    #     if not kl_type:
    #         kl_type = Parser.basic_type_map[canon_type.kind]

    #     if not kl_type:
    #         raise Exception('no KL type for ' + str(canon_type.spelling) + ' ('
    #                         + str(canon_type.kind) + ')')

    #     kl_type = self.get_kl_class_name(kl_type)

    #     if is_array:
    #         kl_type += '[]'

    #     return kl_type

    def abort_on_type(self, kl_type):
        if not kl_type:
            return False
        if '<' in kl_type and kl_type.find('std::vector<') == -1:
            return True
        if '::' in kl_type:
            return True
        if 'const ' in kl_type:
            return True
        if 'type-parameter-' in kl_type:
            return True
        if kl_type.find('[]') != -1:
            return self.abort_on_type(kl_type.replace('[]', ''))
        return False

    @staticmethod
    def is_pointer_type(clang_type):
        canon_type = clang_type.get_canonical()
        if canon_type.kind in [TypeKind.LVALUEREFERENCE, TypeKind.POINTER]:
            return True
        return False

    @staticmethod
    def is_io_param(clang_type):
        canon_type = clang_type.get_canonical()
        #if canon_type.kind in [TypeKind.LVALUEREFERENCE, TypeKind.POINTER]:
        if canon_type.kind in [TypeKind.POINTER]:
            if canon_type.is_const_qualified():
                return False
            return True
        return False

    @staticmethod
    def get_cpp_qual_type_name(clang_type):
        return clang_type.get_canonical().spelling

    def get_cpp_base_type_name(self, clang_type):
        canon_type = clang_type.get_canonical()

        if canon_type.kind == TypeKind.LVALUEREFERENCE:
            return self.get_cpp_base_type_name(canon_type.get_pointee())

        base_name = canon_type.spelling
        if canon_type.is_const_qualified():
            base_name = base_name[len('const '):]
        return base_name

    @staticmethod
    def debug_print(cursor, prefix=''):
        print prefix + str(cursor.kind) + ': ' + str(cursor.spelling)
        for c in cursor.get_children():
            Parser.debug_print(c, prefix + '  ')

    @staticmethod
    def print_diag(diag):
        msg = 'compile '
        if diag.severity >= clang.cindex.Diagnostic.Fatal:
            msg += 'FATAL ERROR'
        elif diag.severity >= clang.cindex.Diagnostic.Error:
            msg += 'error'
        elif diag.severity >= clang.cindex.Diagnostic.Warning:
            msg += 'warning'
        elif diag.severity >= clang.cindex.Diagnostic.Note:
            msg += 'note'
        else:
            msg += 'diag'

        print msg + ': ' + diag.spelling + ' : ' + str(diag.location)
        for fix in diag.fixits:
            print '    ' + str(fix)

        if diag.severity >= clang.cindex.Diagnostic.Fatal:
            return False
        return True

    @staticmethod
    def get_location(clang_location):
        return "%s:%u" % (clang_location.file.name, clang_location.line)

    @staticmethod
    def get_nested_name(cursor):
        semantic_parent = cursor.semantic_parent
        if semantic_parent and semantic_parent.kind in [
            CursorKind.NAMESPACE,
            CursorKind.CLASS_DECL,
            CursorKind.STRUCT_DECL,
            ]:
            result = Parser.get_nested_name(semantic_parent)
            result.append(cursor.spelling)
        else:
            result = [cursor.spelling]
        return result;

    @staticmethod
    def get_nested_type_name(clang_type):
        return Parser.get_nested_name(clang_type.get_declaration())

    @staticmethod
    def get_qualified_spelling(cursor, separator):
        semantic_parent = cursor.semantic_parent
        if semantic_parent:
            if semantic_parent.kind in [
                CursorKind.NAMESPACE,
                CursorKind.CLASS_DECL,
                CursorKind.STRUCT_DECL,
                ]:
                return Parser.get_qualified_spelling(semantic_parent, separator) + separator + cursor.spelling
        return cursor.spelling
            
    def output_class(self, class_name, parent_name, fh):
        fh.write('struct %s' % class_name)
        if parent_name:
            fh.write(' : ' + parent_name)
        fh.write('\n{\n')
        if not parent_name:
            fh.write('  private Data handle;\n')
        fh.write('};\n\n')

    def get_symbol_name(self, kl_class_name, method_name):
        if method_name == '<':
            method_name = kl_class_name + '__lt'
        elif method_name == '<=':
            method_name = kl_class_name + '__le'
        elif method_name == '==':
            method_name = kl_class_name + '__eq'
        elif method_name == '!=':
            method_name = kl_class_name + '__ne'
        elif method_name == '>=':
            method_name = kl_class_name + '__ge'
        elif method_name == '>':
            method_name = kl_class_name + '__gt'
        symbol_name = self.config['extname'] + '_' + method_name.replace('.', '_')
        if symbol_name in self.symbol_names:
            try_name = symbol_name
            i = 0
            while try_name in self.symbol_names:
                try_name = symbol_name + str(i)
                i += 1
            symbol_name = try_name
        self.symbol_names.add(symbol_name)
        return symbol_name

    def output_method(
        self, class_name, rval_type, method_name, params,
        symbol_name, this_usage,
        fh,
        ):
        if rval_type:
            fh.write(rval_type + ' ')
        fh.write(method_name)
        if this_usage == 'io':
            fh.write('!')
        fh.write('(')
        first = True
        for p in params:
            if not first:
                fh.write(', ')
            first = False
            fh.write(p)
        fh.write(') = "' + symbol_name + '";\n')

    def get_kl_class_name(self, cpp_class_name):
        if cpp_class_name in self.kl_type_mappings:
            return self.kl_type_mappings[cpp_class_name].kl_type_name
        return cpp_class_name

    def get_kl_class_repr(self, cpp_class_name):
        if cpp_class_name in self.kl_type_mappings:
            return self.kl_type_mappings[cpp_class_name].cpp_type_name
        return cpp_class_name

    def is_pointer_repr(self, cpp_class_name):
        if cpp_class_name in self.kl_type_mappings:
            return self.kl_type_mappings[cpp_class_name].is_pointer
        return False

    def output_param_conversion(self, type_name, name, kl_cpp_type,
                                param_cpp_type):
        output = []
        if param_cpp_type.find('std::vector<') != -1:
            param_cpp_type = param_cpp_type[len('std::vector<'):
                                            param_cpp_type.find(',')]
            output += ['std::vector< %s > %s_param;' % (param_cpp_type, name, )
                       ]
            output += ['%s_param.resize(%s.size());' % (name, name, )]
            output += ['for (uint32_t %s_i=0; %s_i < %s.size(); %s_i++)' %
                       (name, name, name, name, )]
            output += ['{']
            output += ['const %s &%s_param_array_item = %s[%s_i];' %
                       (Type.get_cpp_type_name(type_name, None, True), name,
                        name, name, )]
            output += [self.output_param_conversion(type_name,
                                                    name + '_param_array_item',
                                                    kl_cpp_type,
                                                    param_cpp_type)]
            output += ['%s_param[%s_i] = %s_param_array_item_param;' %
                       (name, name, name, )]
            output += ['}']
        elif self.types_manager.uses_returnval(type_name):
            output += ['::%s %s_param = %s;' % (param_cpp_type, name, name, )]
        elif type_name == 'String':
            output += ['::%s %s_param(%s.getCString());' %
                       (param_cpp_type, name, name, )]
        elif self.get_kl_class_repr(type_name) == param_cpp_type:
            output += [
                'if (!%s.handle) throwException("\'%s\' parameter is null");' %
                (name, name, )
            ]
            output += ['::%s &%s_param = *(::s *)( %s.handle );'
                       % (self.get_kl_class_name(type_name), name,
                          self.get_kl_class_repr(type_name), name, )]
            if self.is_pointer_repr(type_name):
                output += [
                    'if (!%s_param) throwException("\'%s\' parameter is null");'
                    % (name, name, )
                ]
        else:
            output += [
                'if (!%s.handle) throwException("\'%s\' parameter is null");' %
                (name, name, )
            ]
            output += [
                '::%s &%s_param_handle = *(::%s *)( %s.handle );'
                % (self.get_kl_class_repr(type_name), name,
                   self.get_kl_class_repr(type_name), name, )
            ]
            if self.is_pointer_repr(type_name):
                output += [
                    'if (!%s_param_handle) throwException("\'%s\' parameter is null");'
                    % (name, name, )
                ]
            output += ['::%s %s_param = %s_param_handle;' %
                       (param_cpp_type, name, name, )]
        return '\n'.join(output)

    def output_param_reconversion(self, type_name, name, param_cpp_type):
        output = []
        if param_cpp_type.find('std::vector<') != -1:
            param_cpp_type = param_cpp_type[len('std::vector<'):
                                            param_cpp_type.find(',')]
            output += ['%s.resize(%s_param.size());' % (name, name, )]
            output += ['for (uint32_t %s_i=0; %s_i < %s.size(); %s_i++)' %
                       (name, name, name, name, )]
            output += ['{']
            output += ['::%s %s_param_array_item;' %
                       (Type.get_cpp_type_name(type_name, None, True), name, )]
            output += ['::%s &%s_param_array_item_param = %s_param[%s_i];' %
                       (param_cpp_type, name, name, name, )]
            output += [self.output_param_reconversion(
                type_name, name + '_param_array_item', param_cpp_type)]
            output += ['%s[%s_i] = %s_param_array_item;' % (name, name, name, )
                       ]
            output += ['}']
        elif self.types_manager.uses_returnval(type_name):
            output += ['%s  = %s_param;' % (name, name, )]
        elif type_name == 'String':
            output += ['%s = %s_param;' % (name, name, )]
        else:
            output += ['::%s *%s_result = new ::%s();' %
                       (self.get_kl_class_repr(type_name), name,
                        self.get_kl_class_repr(type_name), )]
            output += ['*%s_result = %s_param;' % (name, name, )]
            output += ['%s.handle = reinterpret_cast<KL::Data>(%s_result);' %
                       (name, name, )]
        return '\n'.join(output)

    def parse_type_decl(self, header, indent, cursor, typemap):
        # no children -> forward declaration
        if len(list(cursor.get_children())) < 1:
            print "%s-> no children" % indent
            return

        cpp_desired_type_name = self.get_qualified_spelling(cursor, "::")
        if cpp_desired_type_name in self.kl_type_mappings:
            kl_type_mapping = self.kl_type_mappings[cpp_desired_type_name]
        else:
            kl_type_mapping = KLTypeMapping(
                self.get_qualified_spelling(cursor, "_"),
                "::" + cpp_desired_type_name,
                )
            self.kl_type_mappings[cpp_desired_type_name] = kl_type_mapping
            self.known_types.add(kl_type_mapping.kl_type_name)

        kl_type = KLStruct(
            kl_type_mapping.kl_type_name,
            kl_type_mapping.cpp_type_name,
            )
        kl_type.codegen.cpp_base_type = kl_type_mapping.cpp_type_name
        kl_type.codegen.header = header

        self.parse_type_decl_children(
            " "+indent,
            cursor,
            typemap,
            kl_type,
            kl_type_mapping.kl_type_name,
            )

        self.types_manager.types[kl_type_mapping.kl_type_name] = kl_type

    @staticmethod
    def print_skipping(function, reason):
        print 'skipping function: ' + function
        print '  since: %s' % reason

    def parse_clang_type(self, clang_type):
        clang_type_kind = clang_type.kind
        if clang_type_kind == TypeKind.VOID:
            return None
        elif clang_type_kind == TypeKind.FLOAT:
            return self.types_manager.Float32, 'in'
        # elif clang_type_kind == TypeKind.LVALUEREFERENCE:
        #     nested_kl_type, nested_kl_usage = self.parse_clang_type(clang_type.get_pointee())
        #     if nested_kl_usage == 'io':
        #         raise Exception('unparsable type')
        #     return nested_kl_type, 'io'
        # elif clang_type_kind == TypeKind.RECORD:
        #     cpp_type_name = clang_type.spelling
        #     kl_type_name = self.kl_type_mappings[cpp_type_name].kl_type_name
        #     kl_type = self.types_manager.types[kl_type_name]
        #     return kl_type, 'in'
        else:
            raise Exception("unhandled type: %s" % str(clang_type.spelling))

    def parse_clang_param(self, clang_param):
        param_name = clang_param.spelling
        if not param_name:
            param_name = 'param' + str(i)

        param_kl_type, param_kl_usage = self.parse_clang_type(clang_param.type)
        
        return param_name, param_kl_type, param_kl_usage

    def parse_type_decl_children(
        self,
        child_indent,
        cursor,
        typemap,
        kl_type,
        kl_class_name,
        include_constructors=True
        ):
        for child in cursor.get_children():
            print "%sparse_CLASS_DECL_children %s" % (child_indent, str(child.kind))

            if child.access_specifier != AccessSpecifier.PUBLIC:
                continue

            is_method = False

            if child.kind == CursorKind.CXX_BASE_SPECIFIER:
                cpp_class_name = self.parse_CLASS_DECL(
                    child_indent,
                    child.get_definition(),
                    child.get_definition().location.file.name
                    )
                parent_class_name = self.get_kl_class_name(cpp_class_name)
                kl_type.parent = parent_class_name

            elif child.kind in [
                CursorKind.CXX_METHOD,
                CursorKind.CONSTRUCTOR,
                CursorKind.DESTRUCTOR,
                CursorKind.FUNCTION_TEMPLATE,
                ]:
                is_method = True
                if clang.cindex.conf.lib.clang_CXXMethod_isPureVirtual(child):
                    kl_type.codegen.is_abstract = True

            if is_method:
                try:
                    result_kl_type = self.parse_clang_type(child.result_type)
                except Exception as e:
                    self.print_skipping(
                        child.displayname,
                        "child result type '%s' is not defined" % child.result_type.spelling
                        )
                    continue

                # if child.spelling in self.skip_methods:
                #     self.print_skipping(
                #         child.displayname,
                #         "method is in skip list"
                #         )
                #     continue

                # if self.abort_on_type(result_kl_type):
                #     self.print_skipping(
                #         child.displayname,
                #         "result type '%s' is in abort list" % result_kl_type
                #         )
                #     continue

                this_usage = 'in'
                if not child.is_static_method():
                    if not child.kind == CursorKind.DESTRUCTOR and not child.kind == CursorKind.CONSTRUCTOR:
                        this_usage = 'in' if child.type.spelling.endswith(
                            'const') else 'io'
                method = Method(child.spelling, result_kl_type, this_usage,
                                'public')
                method.codegen.cpp_qual_ret_type = self.get_cpp_qual_type_name(
                    child.result_type)
                method.codegen.cpp_base_ret_type = self.get_cpp_base_type_name(
                    child.result_type)

                if result_kl_type == 'Data':
                    continue

                operator = None
                if child.kind == CursorKind.DESTRUCTOR:
                    # destructor will be run by the KL destructor in C++
                    continue
                elif child.kind == CursorKind.CONSTRUCTOR:
                    if not include_constructors:
                        continue
                    method_name = child.spelling
                    method.codegen.is_constructor = True
                    num_params = 0
                    for p in child.get_children():
                        if p.kind == CursorKind.PARM_DECL:
                            num_params += 1
                    if num_params == 0:
                        kl_type.codegen.has_empty_constructor = True
                else:
                    if child.is_static_method():
                        method_name = kl_class_name + '_' + child.spelling
                        method.codegen.is_static = True
                        namespace = self.get_namespace(child)
                        if namespace:
                            namespace = '::'.join(namespace)
                        method.codegen.cpp_function = namespace
                    else:
                        if child.spelling.startswith('operator'):
                            operator = child.spelling[len('operator'):]
                            if operator not in ['<', '<=', '==', '!=', '>=',
                                                '>']:
                                self.print_skipping(
                                    child.displayname,
                                    "operator %s is unsupported" % operator
                                    )
                                continue
                            method_name = operator
                            method.codegen.cpp_function = child.spelling
                        else:
                            method_name = kl_class_name + '.' + child.spelling
                            method.codegen.cpp_function = child.spelling

                method.codegen.kl_full_name = method_name

                i = 0
                skip = False
                for p in child.get_children():
                    if p.kind == CursorKind.PARM_DECL:
                        # has_default_value = False
                        # invalid_type = False
                        # try:
                        #     kl_type = self.get_kl_type(p.type)
                        # except Exception as _e:
                        #     invalid_type = True
                        # if invalid_type or self.abort_on_type(kl_type):
                        #     for pc in p.get_children():
                        #         # if it has a default value we'll try to go on from here
                        #         if pc.kind in [
                        #             CursorKind.UNEXPOSED_EXPR,
                        #             CursorKind.INTEGER_LITERAL,
                        #             CursorKind.FLOATING_LITERAL,
                        #             CursorKind.STRING_LITERAL,
                        #             CursorKind.CXX_BOOL_LITERAL_EXPR,
                        #             CursorKind.CXX_NULL_PTR_LITERAL_EXPR,
                        #             CursorKind.DECL_REF_EXPR
                        #         ]:
                        #             has_default_value = True
                        #             break
                        #     if has_default_value:
                        #         break
                        #     skip = True
                        #     break
                        name, kl_type, kl_usage = self.parse_clang_param(p)
                        param = KLParam(name, kl_type, kl_usage)
                        param.codegen.cpp_qual_type = kl_type.cpp_type_name
                        param.codegen.cpp_base_type = kl_type.cpp_type_name
                        method.params.append(param)
                        i += 1

                if skip:
                    self.print_skipping(
                        child.displayname,
                        "unsupported default value"
                        )
                    continue

                symbol_name = self.get_symbol_name(kl_class_name, method_name)
                method.symbol = symbol_name
                method.codegen.is_operator = operator

                kl_type.methods.append(method)

    def output_cpp(
        self,
        kl_type,
        snippets,
        ):
        snippets.append(self.jinjenv.get_template('type.template.cpp').render({
            't': kl_type,
            'header': kl_type.codegen.header,
            'manager': self.types_manager,
            'parser': self,
            'enter': self.cpp_enter,
            'leave': self.cpp_leave,
            }))

    def dump_cursor(self, indent, cursor):
        print indent + str(cursor.kind) + " " + cursor.displayname
        print indent + str(cursor.location)
        childIndent = indent + "."
        for childCursor in cursor.get_children():
            self.dump_cursor(childIndent, childCursor)

    def parse_CLASS_DECL(self, include_filename, indent, current_namespace_path, cursor):
        nested_class_name = self.namespace_mgr.get_nested_type_name(current_namespace_path, cursor.spelling)
        print "%sCLASS_DECL %s" % (indent, "::".join(nested_class_name))
        self.parse_record_decl(include_filename, indent, current_namespace_path, cursor, nested_class_name)

    def parse_STRUCT_DECL(self, include_filename, indent, current_namespace_path, cursor):
        nested_struct_name = self.namespace_mgr.get_nested_type_name(current_namespace_path, cursor.spelling)
        print "%sSTRUCT_DECL %s" % (indent, "::".join(nested_struct_name))
        self.parse_record_decl(include_filename, indent, current_namespace_path, cursor, nested_struct_name)

    def parse_record_decl(self, include_filename, indent, current_namespace_path, cursor, nested_record_name):
        clang_members = []
        clang_static_methods = []
        clang_instance_methods = []

        for child in cursor.get_children():
            if child.kind == CursorKind.FIELD_DECL:
                print "%s  FIELD_DECL %s" % (indent, child.displayname)
                clang_members.append(child)
                continue

            if child.access_specifier != AccessSpecifier.PUBLIC:
                continue

            # if child.kind == CursorKind.CXX_BASE_SPECIFIER:
            #     cpp_class_name = self.parse_CLASS_DECL(
            #         child_indent,
            #         child.get_definition(),
            #         child.get_definition().location.file.name
            #         )
            #     parent_class_name = self.get_kl_class_name(cpp_class_name)
            #     kl_type.parent = parent_class_name

            if child.kind == CursorKind.CXX_METHOD:
                print "%s  CXX_METHOD %s" % (indent, child.displayname)
                if child.is_static_method():
                    clang_static_methods.append(child)
                elif child.spelling.startswith("operator"):
                    pass
                else:
                    clang_instance_methods.append(child)
                continue

                # result_type_info = self.type_mgr.get_type_info(child.result_type)
                # print "result_type_info = " + str(result_type_info)

                # is_const = child.type.spelling.endswith('const')
                # print "this_cpp_type_name = " + child.type.spelling
                # # this_type_info = self.type_mgr.get_type_info(

                # if child.is_static_method():
                #     continue

                # if child.spelling in self.skip_methods:
                #     self.print_skipping(
                #         child.displayname,
                #         "method is in skip list"
                #         )
                #     continue

                # if self.abort_on_type(result_kl_type):
                #     self.print_skipping(
                #         child.displayname,
                #         "result type '%s' is in abort list" % result_kl_type
                #         )
                #     continue

                # this_usage = 'in'
                # if not child.is_static_method():
                #     if not child.kind == CursorKind.DESTRUCTOR and not child.kind == CursorKind.CONSTRUCTOR:
                #         this_usage = 'in' if child.type.spelling.endswith(
                #             'const') else 'io'
                # method = Method(child.spelling, result_kl_type, this_usage,
                #                 'public')
                # method.codegen.cpp_qual_ret_type = self.get_cpp_qual_type_name(
                #     child.result_type)
                # method.codegen.cpp_base_ret_type = self.get_cpp_base_type_name(
                #     child.result_type)

                # if result_kl_type == 'Data':
                #     continue

                # operator = None
                # if child.kind == CursorKind.DESTRUCTOR:
                #     # destructor will be run by the KL destructor in C++
                #     continue
                # elif child.kind == CursorKind.CONSTRUCTOR:
                #     if not include_constructors:
                #         continue
                #     method_name = child.spelling
                #     method.codegen.is_constructor = True
                #     num_params = 0
                #     for p in child.get_children():
                #         if p.kind == CursorKind.PARM_DECL:
                #             num_params += 1
                #     if num_params == 0:
                #         kl_type.codegen.has_empty_constructor = True
                # else:
                #     if child.is_static_method():
                #         method_name = kl_class_name + '_' + child.spelling
                #         method.codegen.is_static = True
                #         namespace = self.get_namespace(child)
                #         if namespace:
                #             namespace = '::'.join(namespace)
                #         method.codegen.cpp_function = namespace
                #     else:
                #         if child.spelling.startswith('operator'):
                #             operator = child.spelling[len('operator'):]
                #             if operator not in ['<', '<=', '==', '!=', '>=',
                #                                 '>']:
                #                 self.print_skipping(
                #                     child.displayname,
                #                     "operator %s is unsupported" % operator
                #                     )
                #                 continue
                #             method_name = operator
                #             method.codegen.cpp_function = child.spelling
                #         else:
                #             method_name = kl_class_name + '.' + child.spelling
                #             method.codegen.cpp_function = child.spelling

                # method.codegen.kl_full_name = method_name

                # i = 0
                # skip = False
                # for p in child.get_children():
                #     if p.kind == CursorKind.PARM_DECL:
                #         # has_default_value = False
                #         # invalid_type = False
                #         # try:
                #         #     kl_type = self.get_kl_type(p.type)
                #         # except Exception as _e:
                #         #     invalid_type = True
                #         # if invalid_type or self.abort_on_type(kl_type):
                #         #     for pc in p.get_children():
                #         #         # if it has a default value we'll try to go on from here
                #         #         if pc.kind in [
                #         #             CursorKind.UNEXPOSED_EXPR,
                #         #             CursorKind.INTEGER_LITERAL,
                #         #             CursorKind.FLOATING_LITERAL,
                #         #             CursorKind.STRING_LITERAL,
                #         #             CursorKind.CXX_BOOL_LITERAL_EXPR,
                #         #             CursorKind.CXX_NULL_PTR_LITERAL_EXPR,
                #         #             CursorKind.DECL_REF_EXPR
                #         #         ]:
                #         #             has_default_value = True
                #         #             break
                #         #     if has_default_value:
                #         #         break
                #         #     skip = True
                #         #     break
                #         name, kl_type, kl_usage = self.parse_clang_param(p)
                #         param = KLParam(name, kl_type, kl_usage)
                #         param.codegen.cpp_qual_type = kl_type.cpp_type_name
                #         param.codegen.cpp_base_type = kl_type.cpp_type_name
                #         method.params.append(param)
                #         i += 1

                # if skip:
                #     self.print_skipping(
                #         child.displayname,
                #         "unsupported default value"
                #         )
                #     continue

                # symbol_name = self.get_symbol_name(kl_class_name, method_name)
                # method.symbol = symbol_name
                # method.codegen.is_operator = operator

                # kl_type.methods.append(method)

        members = []
        for clang_member in clang_members:
            member = Member(
                self.type_mgr.get_dqti(
                    self.namespace_mgr.get_nested_type_name(current_namespace_path, clang_member.type)
                    ),
                clang_member.displayname,
                clang_member.access_specifier == AccessSpecifier.PUBLIC,
                )
            members.append(member)

        can_in_place = all(member and member.can_in_place for member in members)
        if can_in_place:
            self.type_mgr.add_selector(
                InPlaceStructSelector(
                    self.jinjenv,
                    nested_record_name,
                    )
                )
        else:
            self.type_mgr.add_selector(
                WrappedPtrSelector(
                    self.jinjenv,
                    nested_record_name,
                    )
                )

        this_type_info = self.type_mgr.get_dqti(nested_record_name).type_info

        instance_methods = [
            InstanceMethod(
                self.type_mgr,
                self.namespace_mgr,
                current_namespace_path,
                this_type_info,
                clang_instance_method,
                )
            for clang_instance_method in clang_instance_methods
            ]

        if can_in_place:
            self.edk_decls.add(
                ast.Wrapping(
                    self.config['extname'],
                    include_filename,
                    self.get_location(cursor.location),
                    cursor.displayname,
                    this_type_info,
                    members,
                    instance_methods,
                    "ast/builtin/in_place_struct_decl",
                    )
                )
        else:
            self.edk_decls.add(
                ast.Wrapping(
                    self.config['extname'],
                    include_filename,
                    self.get_location(cursor.location),
                    cursor.displayname,
                    this_type_info,
                    members,
                    instance_methods,
                    "ast/builtin/wrapped_ptr_decl",
                    )
                )

    def parse_MACRO_INSTANTIATION(self, include_filename, indent, current_namespace_path, cursor):
        print dir(cursor)
        self.dump_cursor(indent, cursor)
        print indent + ".get_definition() ->"
        self.dump_cursor(indent + ' ', cursor.get_definition())

    def parse_TYPEDEF_DECL(self, include_filename, indent, current_namespace_path, cursor):
        new_cpp_type_name = cursor.type.spelling
        nested_new_cpp_type_name = current_namespace_path + [new_cpp_type_name]
        old_cpp_type_name = cursor.underlying_typedef_type.spelling
        if old_cpp_type_name.startswith("struct "):
            old_cpp_type_name = old_cpp_type_name[7:]
        nested_old_cpp_type_name = self.namespace_mgr.get_nested_type_name(current_namespace_path, old_cpp_type_name)
        print "%sTYPEDEF_DECL %s -> %s" % (indent, "::".join(nested_new_cpp_type_name), "::".join(nested_old_cpp_type_name))
        new_type_info, old_type_info = self.type_mgr.add_type_alias(nested_new_cpp_type_name, nested_old_cpp_type_name)
        if new_type_info and old_type_info:
            self.edk_decls.add(
                ast.Alias(
                    self.config['extname'],
                    include_filename,
                    self.get_location(cursor.location),
                    cursor.displayname,
                    new_type_info,
                    old_type_info,
                    )
                )

    def parse_FUNCTION_DECL(self, include_filename, indent, current_namespace_path, cursor):
        nested_name = current_namespace_path + [cursor.spelling]
        print "%sFUNCTION_DECL %s" % (indent, "::".join(nested_name))

        if True:
        # try:
            param_index = 1
            params = []
            for param_cursor in cursor.get_children():
                if param_cursor.kind == CursorKind.PARM_DECL:
                    param_name = param_cursor.spelling
                    if len(param_name) == 0:
                        param_name = "_param_%u" % param_index
                    nested_param_type_name = self.namespace_mgr.get_nested_type_name(current_namespace_path, param_cursor.type)
                    params.append(ParamCodec(
                        self.type_mgr.get_dqti(nested_param_type_name),
                        param_name,
                        ))
                param_index += 1

            nested_result_type_name = self.namespace_mgr.get_nested_type_name(current_namespace_path, cursor.result_type)

            self.edk_decls.add(
                ast.Func(
                    self.config['extname'],
                    include_filename,
                    self.get_location(cursor.location),
                    cursor.displayname,
                    nested_name,
                    self.type_mgr.get_dqti(nested_result_type_name),
                    params,
                    )
                )
        # except Exception as e:
        #     print "%s Unable to wrap function: %s" % (indent, str(e))

    ignored_cursor_kinds = [
        CursorKind.MACRO_DEFINITION,
        CursorKind.INCLUSION_DIRECTIVE,
        ]

    def parse_cursor(self, include_filename, indent, current_namespace_path, cursor):
        cursor_kind = cursor.kind
        if cursor_kind in Parser.ignored_cursor_kinds:
            pass
        elif cursor_kind == CursorKind.NAMESPACE:
            nested_namespace_name = cursor.spelling
            nested_namespace_path = self.namespace_mgr.add_nested_namespace(
                current_namespace_path,
                nested_namespace_name,
                )
            self.parse_children(include_filename, indent, nested_namespace_path, cursor)
        elif cursor_kind == CursorKind.UNEXPOSED_DECL:
            self.parse_children(include_filename, indent, current_namespace_path, cursor)
        elif cursor_kind == CursorKind.MACRO_INSTANTIATION:
            self.parse_MACRO_INSTANTIATION(include_filename, indent, current_namespace_path, cursor)
        elif cursor_kind == CursorKind.TYPEDEF_DECL:
            self.parse_TYPEDEF_DECL(include_filename, indent, current_namespace_path, cursor)
        elif cursor_kind == CursorKind.CLASS_DECL:
            self.parse_CLASS_DECL(include_filename, indent, current_namespace_path, cursor)
        elif cursor_kind == CursorKind.STRUCT_DECL:
            self.parse_STRUCT_DECL(include_filename, indent, current_namespace_path, cursor)
        elif cursor_kind == CursorKind.FUNCTION_DECL:
            self.parse_FUNCTION_DECL(include_filename, indent, current_namespace_path, cursor)
        else:
            print "%sUnhandled %s" % (indent, cursor_kind)

    def parse_children(self, include_filename, childIndent, current_namespace_path, cursor):
        for childCursor in cursor.get_children():
            self.parse_cursor(include_filename, childIndent, current_namespace_path, childCursor)

    def parse(self, unit_filename):
        print "parsing unit: %s" % unit_filename

        clang_index = clang.cindex.Index.create()
        unit = clang_index.parse(
            unit_filename,
            self.config['clang_opts'],
            None,
            clang.cindex.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES,
            # clang.cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD
            )

        skip = False
        for d in unit.diagnostics:
            skip = skip or not self.print_diag(d)

        if skip:
            print 'skipping unit: ' + unit.spelling
        else:
            for cursor in unit.cursor.get_children():
                if hasattr(cursor.location.file, 'name') and cursor.location.file.name != unit_filename:
                    continue
                self.parse_cursor(unit_filename, "", [], cursor)

    def output_kl_type(
        self,
        kl_type_name,
        visited_kl_type_names,
        fh_kl,
        snippets,
        ):
        print "output_kl_type %s" % kl_type_name
        if kl_type_name not in visited_kl_type_names:
            visited_kl_type_names.add(kl_type_name)
            kl_type = self.types_manager.types[kl_type_name]

            parent_kl_type_name = kl_type.parent
            if parent_kl_type_name:
                parent_kl_type = self.types_manager.types[parent_kl_type_name]

                self.output_kl_type(
                    parent_kl_type_name,
                    visited_kl_type_names,
                    fh_kl,
                    snippets,
        		    )
            
            self.output_class(kl_type_name, parent_kl_type_name, fh_kl)

            for m in kl_type.methods:
                params = []

                if m.codegen.is_operator:
                    params.append('in ' + kl_type_name + ' this_')

                for p in m.params:
                    param_type = p.type_name
                    if p.arraymod:
                        param_type += p.arraymod
                    params.append(p.usage + ' ' + param_type + ' ' + p.name)

                self.output_method(
                    kl_type_name,
                    m.ret_type_name,
                    m.codegen.kl_full_name,
                    params,
                    m.symbol,
                    m.usage,
                    fh_kl,
                    )

            if not kl_type.codegen.is_abstract:
                self.output_method(
                    kl_type_name,
                    None,
                    '~' + kl_type_name,
                    [],
                    kl_type_name + '__destructor',
                    'in',
                    fh_kl,
                    )
                self.output_method(
                    kl_type_name,
                    None,
                    kl_type_name,
                    ['in ' + kl_type_name + ' that'],
                    kl_type_name + '__copy_constructor',
                    'in',
                    fh_kl,
                    )
                self.output_method(
                    kl_type_name,
                    None,
                    kl_type_name + '.=',
                    ['in ' + kl_type_name + ' that'],
                    kl_type_name + '__copy_constructor',
                    'in',
                    fh_kl,
                    )

            self.output_cpp(kl_type, snippets['cpp'])

    def jinja_stream(self, lang):
        return self.jinjenv.get_template("ast/builtin/template." + lang).stream(
            ext_name = self.config['extname'],
            gen_decl_streams = lambda: self.edk_decls.jinja_streams(self.jinjenv, lang),
            )
    
    def output(
        self,
        output_kl_filename,
        output_cpp_filename,
        ):
        # # prune types without full definitions
        # for kl_type_name in self.types_manager.types:
        #     kl_struct = self.types_manager.types[kl_type_name]
        #     methods = []
        #     for m in kl_struct.methods:
        #         remove = False
        #         for p in m.params:
        #             if not p.kl_type_name in self.known_types:
        #                 remove = True

        #         if m.ret_type_name and not m.ret_type_name.replace(
        #             '[]', '') in self.known_types:
        #             remove = True

        #         if not remove:
        #             methods.append(m)

        #     kl_struct.methods = methods

        self.jinja_stream('kl').dump(output_kl_filename)
        self.jinja_stream('cpp').dump(output_cpp_filename)
