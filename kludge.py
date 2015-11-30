import lib_parser, optparse, sys, os

def parse_main():
    try:
        opt_parser = optparse.OptionParser(
            usage='Usage: %prog [options] <EXTNAME> <input.h> [<input2.h> ...]'
            )
        opt_parser.add_option(
            '-o', '--outdir',
            action='store',
            default='.',
            dest='outdir',
            metavar='OUTDIR',
            help="output directory",
            )
        opt_parser.add_option(
            '-b', '--basename',
            action='store',
            default='',
            dest='basename',
            metavar='BASENAME',
            help="output to OUTDIR/BASENAME.{kl,cpp} (defaults to EXTNAME)",
            )
        opt_parser.add_option(
            '-p', '--pass',
            action='append',
            dest='clang_opts',
            metavar='CLANGOPT',
            help="pass option to clang++ (can be used multiple times)",
            )
        (opts, args) = opt_parser.parse_args()
        if len(args) < 2:
            raise Exception("At least one input file is required")
    except Exception as e:
        print "Error: %s" % str(e)
        print "Run '%s --help' for usage" % sys.argv[0]
        sys.exit(1)

    extname = args[0]
    if len(opts.basename) > 0:
        basename = opts.basename
    else:
        basename = extname

    parser = lib_parser.LibParser(opts.clang_opts)
    for i in range(1, len(args)):
        parser.parse(args[i])
    parser.output(
        os.path.join(opts.outdir, basename + '.kl'),
        os.path.join(opts.outdir, basename + '.cpp'),
        )

parse_main()
