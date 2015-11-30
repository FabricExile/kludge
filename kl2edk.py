#!/usr/bin/env python

import FabricEngine.Core
import hashlib, jinja2, optparse, os, sys, traceback

try:
    import ujson as json
except Exception:
    print 'WARNING: falling back to standard json module, please install ujson for improved performance'
    import json


class Alias:
    def __init__(self, oldname, newname):
        self.newname = newname
        self.oldname, self.arraymod = Type.extract_type_name_arraymod(oldname)

    @property
    def oldname_cpp(self):
        return Type.get_cpp_type_name(self.oldname, self.arraymod)

    @property
    def oldname_cpp_full(self):
        return Type.get_cpp_type_name(self.oldname, self.arraymod, True)


class Require:
    def __init__(self, name, version_range):
        self.name = name
        self.version_range = version_range
        self.maj = 0
        self.min = 0
        self.bugfix = 0


class Type:
    class CodeGenOpts:
        def __init__(self):
            self.cpp_base_type = None
            self.cpp_qual_type = None
            self.has_empty_constructor = False
            self.is_abstract = False
            self.header = None

    def __init__(self, type_name):
        self.type_name = type_name
        self.members = []
        self.methods = []
        self.codegen = Type.CodeGenOpts()

    def hash(self):
        m = hashlib.md5()
        m.update(self.type_name)
        return m.hexdigest()

    @property
    def type_name_cpp(self):
        return Type.get_cpp_type_name(self.type_name, None)

    @property
    def type_name_cpp_full(self):
        return Type.get_cpp_type_name(self.type_name, None, True)

    @staticmethod
    def get_cpp_usage(usage):
        if usage == 'io':
            return 'IOParam'
        elif usage == 'in':
            return 'INParam'
        elif usage == 'out':
            return 'OUTParam'
        else:
            raise Exception('invalid usage: ' + usage)

    @staticmethod
    def get_cpp_type_name(type_name, arraymod=None, full=False):
        if not type_name:
            return None
        prefix = ''
        if full:
            prefix = 'Fabric::EDK::KL::'
        if not arraymod:
            return prefix + type_name
        elif arraymod[:2] == '<>':
            return prefix + 'ExternalArray< ' + Type.get_cpp_type_name(
                type_name, arraymod[2:], full) + ' >'
        elif arraymod[:2] == '[]':
            return prefix + 'VariableArray< ' + Type.get_cpp_type_name(
                type_name, arraymod[2:], full) + ' >'
        else:
            start = arraymod.find('[') + 1
            end = arraymod.find(']')
            index = arraymod[start:end]
            if index.isnumeric():
                return prefix + 'FixedArray< ' + Type.get_cpp_type_name(
                    type_name, arraymod[end + 1:], full) + ', ' + index + ' >'
            else:
                return 'Dict< ' + prefix + index + ', ' + Type.get_cpp_type_name(
                    type_name, arraymod[end + 1:], full) + ' >'

    @staticmethod
    def extract_type_name(full_type_name):
        if not full_type_name:
            return None
        name = full_type_name
        if name.startswith('Ref<'):
            name = name[4:-1]
        return name

    @staticmethod
    def extract_type_name_arraymod(full_type_name):
        name = Type.extract_type_name(full_type_name)
        if not name:
            return None, None
        arraymod = None
        lastchar = name[-1:]
        if lastchar == '>':
            arraymod = '<>'
            name = name[:-2]
        elif lastchar == ']':
            firstindex = name.index('[')
            arraymod = name[firstindex:]
            name = name[0:firstindex]
        return name, arraymod


class BaseType(Type):
    def __init__(self, name):
        Type.__init__(self, name)


class Object(Type):
    def __init__(self, name):
        Type.__init__(self, name)
        self.parent = None
        self.interfaces = []


class Struct(Type):
    def __init__(self, name):
        Type.__init__(self, name)
        self.parent = None


class Interface(Type):
    def __init__(self, name):
        Type.__init__(self, name)
        self.interfaces = []


class Member:
    def __init__(self, name, type_name, access, arraymod):
        self.name = name
        self.type_name, maybe_arraymod = Type.extract_type_name_arraymod(type_name)
        self.access = access
        self.arraymod = arraymod

        # this can happen if a member is declared like this for example:
        #   UInt32[] foo, bar[];
        if maybe_arraymod:
            self.arraymod = maybe_arraymod + self.arraymod

    @property
    def type_name_cpp(self):
        return Type.get_cpp_type_name(self.type_name, self.arraymod)

    @property
    def type_name_cpp_full(self):
        return Type.get_cpp_type_name(self.type_name, self.arraymod, True)


class Function:
    class CodeGenOpts:
        def __init__(self):
            self.cpp_function = None

    def __init__(self, name, ret_type_name):
        self.name = name
        self.ret_type_name = Type.extract_type_name(ret_type_name)
        self.ret_type_name_base, self.rtype_arraymod = Type.extract_type_name_arraymod(
            ret_type_name)
        self.params = []
        self.symbol = None
        self.codegen = Function.CodeGenOpts()

    @property
    def ret_type_name_cpp(self):
        return Type.get_cpp_type_name(self.ret_type_name_base,
                                      self.rtype_arraymod)

    @property
    def ret_type_name_cpp_full(self):
        return Type.get_cpp_type_name(self.ret_type_name_base,
                                      self.rtype_arraymod, True)


class Method(Function):
    class CodeGenOpts(Function.CodeGenOpts):
        def __init__(self):
            Function.CodeGenOpts.__init__(self)
            self.is_static = False
            self.is_constructor = False
            self.cpp_base_ret_type = None
            self.cpp_qual_ret_type = None
            self.kl_full_name = None
            self.is_operator = False

    def __init__(self, name, ret_type_name, usage, access):
        Function.__init__(self, name, ret_type_name)
        self.usage = usage
        self.access = access
        self.interface = None
        self.codegen = Method.CodeGenOpts()

    @property
    def usage_cpp(self):
        return Type.get_cpp_usage(self.usage)

    def hash(self):
        m = hashlib.md5()
        if self.ret_type_name:
            m.update(self.ret_type_name)
        m.update(self.name)
        for p in self.params:
            m.update(p.hash())
        return m.hexdigest()


class Param:
    class CodeGenOpts:
        def __init__(self):
            self.cpp_base_type = None
            self.cpp_qual_type = None

    def __init__(self, name, type_name, usage):
        self.name = name
        self.type_name, self.arraymod = Type.extract_type_name_arraymod(type_name)
        self.usage = usage
        self.codegen = Param.CodeGenOpts()

    @property
    def type_name_cpp(self):
        return Type.get_cpp_type_name(self.type_name, self.arraymod)

    @property
    def type_name_cpp_full(self):
        return Type.get_cpp_type_name(self.type_name, self.arraymod, True)

    @property
    def usage_cpp(self):
        return Type.get_cpp_usage(self.usage)

    def hash(self):
        m = hashlib.md5()
        m.update(self.name)
        m.update(self.type_name)
        m.update(self.usage)
        return m.hexdigest()


class TypesManager:
    returnval_types = ['Boolean', 'UInt8', 'UInt16', 'UInt32', 'UInt64',
                       'SInt8', 'SInt16', 'SInt32', 'SInt64', 'Float32',
                       'Float64', 'Byte', 'Size', 'Index', 'Count', 'VBOID',
                       'Data', 'DataSize', 'Integer', 'Scalar']

    def __init__(self, ext_name):
        self.ext_name = ext_name
        self.base_types = {}
        self.types = {}
        self.aliases = {}
        self.requires = {}
        self.functions = []

    def parse(self, ast):
        for global_list in ast:
            for node in global_list:
                try:
                    self.parse_node(node)
                except Exception:
                    print 'node: ' + str(node)
                    print traceback.format_exc()
                    sys.exit(1)

    def parse_node(self, node):
        ntype = node['type']
        if ntype == 'ASTInterfaceDecl':
            self.add_interface(node)
        elif ntype == 'ASTObjectDecl':
            self.add_object(node)
        elif ntype == 'ASTStructDecl':
            self.add_struct(node)
        elif ntype == 'MethodOpImpl':
            self.add_method(node)
        elif ntype == 'Alias':
            self.add_alias(node)
        elif ntype == 'RequireGlobal':
            self.add_require(node)
        elif ntype == 'Destructor':
            self.add_destructor(node)
        elif ntype == 'Function':
            self.add_function(node)
        elif ntype == 'BinOpImpl':
            self.add_binop(node)
        elif ntype == 'ComparisonOpImpl':
            self.add_compareop(node)
        elif ntype == 'GlobalConstDecl':
            pass

    def add_require(self, node):
        for require in node['requires']:
            r = Require(require['name'], require['versionRange'])
            self.requires[require['name']] = r

    def add_alias(self, node):
        oldname = node['oldUserName']
        newname = node['newUserName']
        alias = Alias(oldname, newname)
        self.set_location(alias, node)
        self.aliases[newname] = alias

    def add_destructor(self, node):
        t = self.types[node['thisType']]
        m = Method(node['name'], None, 'io', None)
        self.set_location(m, node)
        if 'symbolName' in node:
            m.symbol = node['symbolName']
        t.methods.append(m)

    def add_function(self, node):
        f = Function(node['name'], node.get('returnType', None))
        self.set_location(f, node)
        for param in node['params']:
            if param['type'] != 'Param':
                raise Exception('bad param type')
            p = Param(param['name'], param['typeUserName'], param['usage'])
            f.params.append(p)
        if 'symbolName' in node:
            f.symbol = node['symbolName']
        self.functions.append(f)

    def add_method(self, node):
        if not node['thisType'] in self.types:
            if not node['thisType'] in self.base_types:
                t = BaseType(node['thisType'])
                self.base_types[node['thisType']] = t
            else:
                t = self.base_types[node['thisType']]
        else:
            t = self.types[node['thisType']]
        m = Method(node['name'], node.get('returnType', None),
                   node['thisUsage'], None)
        self.set_location(m, node)
        for param in node['params']:
            if param['type'] != 'Param':
                raise Exception('bad param type')
            p = Param(param['name'], param['typeUserName'], param['usage'])
            m.params.append(p)
        if 'symbolName' in node:
            m.symbol = node['symbolName']
        t.methods.append(m)

    def add_binop(self, node):
        return_type = node['rhs']['typeUserName']
        f = Function(None, return_type)
        self.set_location(f, node)
        lhs = node['lhs']
        p = Param(lhs['name'], lhs['typeUserName'], lhs['usage'])
        f.params.append(p)
        rhs = node['rhs']
        p = Param(rhs['name'], rhs['typeUserName'], rhs['usage'])
        f.params.append(p)
        if 'symbolName' in node:
            f.symbol = node['symbolName']
        self.functions.append(f)

    def add_compareop(self, node):
        return_type = node['returnType']
        f = Function(None, return_type)
        self.set_location(f, node)
        lhs = node['lhs']
        p = Param(lhs['name'], lhs['typeUserName'], lhs['usage'])
        f.params.append(p)
        rhs = node['rhs']
        p = Param(rhs['name'], rhs['typeUserName'], rhs['usage'])
        f.params.append(p)
        if 'symbolName' in node:
            f.symbol = node['symbolName']
        self.functions.append(f)

    def add_struct(self, node):
        t = Struct(node['name'])
        self.set_location(t, node)
        if 'members' in node:
            self.add_members(t, node['members'])
        t.parent = node.get('parentStructName', None)
        if t.parent:
            t.parent = self.types[t.parent]
        self.set_depends(t)
        self.types[node['name']] = t

    def add_object(self, node):
        t = Object(node['name'])
        self.set_location(t, node)
        if 'members' in node:
            self.add_members(t, node['members'])
        parentsAndInterfaces = node.get('parentsAndInterfaces', [])
        for pi in parentsAndInterfaces:
            if self.is_object(pi):
                t.parent = self.types[pi]
            elif self.is_interface(pi):
                t.interfaces.append(self.types[pi])
            else:
                raise Exception('bad parentsAndInterfaces type: ' + pi)
        self.set_depends(t)
        self.set_interface_methods(t)
        self.types[node['name']] = t

    def add_interface(self, node):
        t = Interface(node['name'])
        self.set_location(t, node)
        if 'members' in node:
            for member in node['members']:
                if member['type'] != 'ASTInterfaceMethod':
                    raise Exception('bad member type: '+member['type'])
                m = Method(member['name'], member.get('returnType', None),
                           member['thisUsage'], member['cgAccess'])
                m.interface = t
                for param in member['params']:
                    if param['type'] != 'Param':
                        raise Exception('bad param type')
                    p = Param(param['name'], param['typeUserName'],
                              param['usage'])
                    m.params.append(p)
                t.methods.append(m)
        self.set_depends(t)
        self.types[node['name']] = t

    @staticmethod
    def add_members(totype, members):
        for member in members:
            if member['type'] != 'MemberGroupDecl':
                raise Exception('bad member type')
            for decl in member['memberDecls']:
                if decl['type'] != 'MemberDecl':
                    raise Exception('bad decl type')
                m = Member(decl['name'], member['baseType'], member['access'],
                           decl['arrayModifier'])
                totype.members.append(m)

    @staticmethod
    def set_location(totype, node):
        totype.location = node['sourceInfo']['file'] + ':' + str(
            node['sourceInfo']['line']) + ':' + str(node['sourceInfo']['column'])

    def set_depends(self, totype):
        depends = set()
        for member in totype.members:
            if self.types.has_key(member.type_name):
                depends.add(member.type_name)
        for method in totype.methods:
            if self.types.has_key(method.ret_type_name):
                depends.add(method.ret_type_name)
            for param in method.params:
                if self.types.has_key(param.type_name):
                    depends.add(param.type_name)
        totype.depends = depends

    @staticmethod
    def set_interface_methods(totype):
        methods = {}
        for interface in totype.interfaces:
            for method in interface.methods:
                if not method.hash() in methods:
                    methods[method.hash()] = method
        totype.interface_methods = methods.values()

    def is_object(self, name):
        return isinstance(self.types.get(name, None), Object)

    def is_interface(self, name):
        return isinstance(self.types.get(name, None), Interface)

    def is_struct(self, name):
        return isinstance(self.types.get(name, None), Struct)

    def is_base_type(self, name):
        return isinstance(self.types.get(name, None), BaseType)

    def get_type(self, name):
        return self.types.get(name, None)

    def uses_returnval(self, name):
        return name in self.returnval_types or name in self.aliases and self.aliases[name].oldname in self.returnval_types


class OutputManager:
    def __init__(self, output_folder):
        self.output_folder = output_folder

    def output_header(self, template, params, basename):
        output = template.render(params)
        path = os.path.join(self.output_folder, basename + '.h')
        header = open(path, 'w')
        header.write(output)
        header.close()

    def output_version_exports(self, symbols):
        output = open(os.path.join(self.output_folder, 'version.exports'), 'w')
        output.write('{\n')
        output.write('  global: FabricEDKInit;')
        if len(symbols) > 0:
            output.write(';'.join(symbols) + ';')
        output.write('\n')
        output.write('  local: *;\n')
        output.write('};')
        output.close()


def main():
    opt_parser = optparse.OptionParser(
        usage='Usage: %prog [options] <file.fpm.json>')
    opt_parser.add_option('-o', '--outputfolder',
                          action='store',
                          dest='output_folder',
                          help='output folder for header files')
    opt_parser.add_option('-i', '--inputfolder',
                          action='store',
                          dest='input_folder',
                          help='base folder for KL files')
    (opts, args) = opt_parser.parse_args()

    if len(args) < 1:
        opt_parser.print_help()
        sys.exit(1)

    fpm_json_file = args[0]

    ext_name = os.path.basename(fpm_json_file).split('.')[0]

    output_folder = opts.output_folder
    input_folder = opts.input_folder

    if not output_folder:
        opt_parser.print_help()
        sys.exit(1)

    fabric_client = FabricEngine.Core.createClient({'noOptimization': True})
    output_manager = OutputManager(output_folder)
    manager = TypesManager(ext_name)

    _, file_ext = os.path.splitext(fpm_json_file)
    if file_ext == '.kl':
        files = [fpm_json_file]
    elif file_ext == '.json':
        fpm_json_data = json.loads(open(fpm_json_file).read())
        files = fpm_json_data['code']
        if not isinstance(files, list):
            files = [files]
    else:
        raise Exception('unrecognized file type: ' + fpm_json_file)

    code = ''
    file_paths = []
    for kl_file in files:
        file_path = kl_file
        if not os.path.exists(file_path):
            file_path = os.path.join(os.path.dirname(fpm_json_file), kl_file)
        if not os.path.exists(file_path) and input_folder:
            file_path = os.path.join(input_folder, kl_file)

        if not os.path.exists(file_path):
            raise Exception('file not found: ' + file_path)

        file_paths.append(file_path)
        code += open(file_path).read()

    # get the full recursive AST for everything used by this extension
    astString = fabric_client.getKLJSONAST('kl2edk.kl', code,
                                           True).getStringCString()
    ast = json.loads(astString)

    if len(ast['diagnostics']) > 0:
        for diag in ast['diagnostics']:
            print diag
        sys.exit(1)

    manager.parse(ast['ast'])

    # this pass could be skipped but is fast as we don't use recursive AST
    # and it allows us to update location information for types to the
    # file and line numbers of their original KL
    for kl_file in file_paths:
        astString = fabric_client.getKLJSONAST(kl_file, open(kl_file).read(),
                                               False).getStringCString()
        ast = json.loads(astString)
        manager.parse([ast['ast']])

    environ = jinja2.Environment(
        trim_blocks=True,
        lstrip_blocks=True,
        loader=jinja2.PackageLoader('__main__', 'templates'))

    (major, minor, bugfix) = fabric_client.build.getPureVersion().split('.')
    base_params = {
        'manager': manager,
        'version_full': fabric_client.build.getFullVersion(),
        'version_maj': major,
        'version_min': minor,
        'version_bugfix': bugfix,
    }

    globalTmpl = environ.get_template('global.template.h')
    output_manager.output_header(globalTmpl, base_params, 'global')

    aliasesTmpl = environ.get_template('aliases.template.h')
    output_manager.output_header(aliasesTmpl, base_params, 'aliases')

    symbols = []
    for f in manager.functions:
        if f.symbol:
            symbols.append(f.symbol)
    if len(symbols) > 0:
        globalFunctionsTmpl = environ.get_template(
            'global_functions.template.h')
        output_manager.output_header(globalFunctionsTmpl, base_params,
                                     'global_functions')

    function_headers = []
    for type_name in manager.types:
        t = manager.types[type_name]

        type_symbols = []
        for m in t.methods:
            if m.symbol:
                type_symbols.append(m.symbol)
        symbols.extend(type_symbols)

        params = base_params
        params['t'] = t

        if manager.is_object(type_name):
            baseTmpl = environ.get_template('object.template.h')
            implTmpl = environ.get_template('object_impl.template.h')
        elif manager.is_interface(type_name):
            baseTmpl = environ.get_template('interface.template.h')
            implTmpl = environ.get_template('interface_impl.template.h')
        elif manager.is_struct(type_name):
            baseTmpl = environ.get_template('struct.template.h')
            implTmpl = None

        output_manager.output_header(baseTmpl, params, t.type_name)
        if implTmpl:
            output_manager.output_header(implTmpl, params,
                                         t.type_name + '_impl')

        if len(type_symbols) > 0:
            functionsTmpl = environ.get_template('type_functions.template.h')
            output_manager.output_header(functionsTmpl, params,
                                         t.type_name + '_functions')
            function_headers.append(t.type_name)
    
    # some extensions may add methods to existing base types, these
    # have to be handled separately from custom registered types
    for type_name in manager.base_types:
        t = manager.base_types[type_name]

        type_symbols = []
        for m in t.methods:
            if m.symbol:
                type_symbols.append(m.symbol)
        symbols.extend(type_symbols)

        params = base_params
        params['t'] = t

        if len(type_symbols) > 0:
            functionsTmpl = environ.get_template('type_functions.template.h')
            output_manager.output_header(functionsTmpl, params,
                                         t.type_name + '_functions')
            function_headers.append(t.type_name)

    params = base_params
    params['function_headers'] = function_headers
    extNameTmpl = environ.get_template('extension.template.h')
    output_manager.output_header(extNameTmpl, params, ext_name)

    output_manager.output_version_exports(symbols)

if __name__ == "__main__":
    main()
