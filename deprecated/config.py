#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import jinja2

def create_default_config():
  return {
    "extname": "",        # must be provided
    "basename": "",       # will default to extname
    "infiles": [],
    "outdir": ".",
    "clang_opts": [
      '-x',
      'c++',
      ],
    }

def create_jinjenv(config):
  return jinja2.Environment(
    trim_blocks=True,
    lstrip_blocks=True,
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
        "ast": jinja2.PrefixLoader({
            "builtin": jinja2.PackageLoader('__main__', 'libkludge/ast'),
            }),
        }),
    undefined = jinja2.StrictUndefined,
    )
