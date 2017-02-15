#!/usr/bin/env python
#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import os, sys, pytest, subprocess, difflib, platform

fabric_scene_graph_dir = os.environ['FABRIC_SCENE_GRAPH_DIR']
if fabric_scene_graph_dir:
  root_dir = os.path.join(fabric_scene_graph_dir, 'Native', 'Tools', 'Kludge')
else:
  root_dir = '.'

fabric_dir = os.environ['FABRIC_DIR']
if fabric_dir:
  kludge = os.path.join(fabric_dir, 'Tools', 'Kludge', 'kludge.py')
else:
  kludge = 'kludge'

test_generate_dir = os.path.join(root_dir, 'test', 'generate')
test_generate_tmp_dir_base = os.path.join(root_dir, 'test', 'tmp', 'generate')

def collect_test_generate_basenames():
  result = []
  for dirpath, _subdirs, filenames in os.walk(test_generate_dir):
      for filename in filenames:
          filebase_and_ext2, fileext1 = os.path.splitext(filename)
          if fileext1 == '.py':
            filebase, fileext2 = os.path.splitext(filebase_and_ext2)
            if fileext2 == '.kludge':
                result.append(filebase)
  return result

@pytest.mark.parametrize("basename", collect_test_generate_basenames())
def test_generate(basename):

  if os.path.isfile(os.path.join(test_generate_dir, basename + '.skip')):
    return

  test_tmp_dir = os.path.join(test_generate_tmp_dir_base, basename)

  if not os.path.isdir(test_tmp_dir):
    os.makedirs(test_tmp_dir)

  assert subprocess.call(
    [
      'python', kludge, 'generate',
      '-o', test_tmp_dir,
      '--debug-type-templates',
      basename,
      os.path.join(test_generate_dir, basename + '.kludge.py'),
      ],
    ) == 0

  scons_env = os.environ.copy()
  scons_env['CPPPATH'] = os.path.abspath(test_generate_dir)
  if platform.system() == 'Windows':
    scons_args = ['scons.bat']
  else:
    scons_args = ['scons']
  scons_args.extend([
    '-f', basename + '.SConstruct',
    ])
  assert subprocess.call(
    scons_args,
    cwd = test_tmp_dir,
    env = scons_env,
    ) == 0

  kl_env = os.environ.copy()
  kl_env['FABRIC_EXTS_PATH'] = test_tmp_dir
  with open(os.path.join(test_tmp_dir, basename + '.test.out')) as expected_kl_output_file:
    expected_kl_output = expected_kl_output_file.read().splitlines()
  actual_kl_output = subprocess.check_output(
    [
      'kl',
      os.path.join(test_tmp_dir, basename + '.test.kl'),
      ],
    env = kl_env,
    ).splitlines()
  actual_kl_output = filter(
    lambda line: not line.startswith('[ST] '),
    actual_kl_output
    )
  difflines = difflib.unified_diff(expected_kl_output, actual_kl_output)
  diffline_count = 0
  for diffline in difflines:
    print diffline
    diffline_count += 1
  assert diffline_count == 0

test_discover_dir = os.path.join('test', 'discover')
test_discover_tmp_dir_base = os.path.join('test', 'tmp', 'discover')

def collect_test_discover_basenames():
  result = []
  for dirpath, _subdirs, filenames in os.walk(test_discover_dir):
      for filename in filenames:
          basename, fileext = os.path.splitext(filename)
          if fileext == '.hpp':
            result.append(basename)
  return result

@pytest.mark.parametrize("basename", collect_test_discover_basenames())
def test_discover(basename):

  if os.path.isfile(os.path.join(test_discover_dir, basename + '.skip')):
    return

  test_tmp_dir = os.path.join(test_discover_tmp_dir_base, basename)

  if not os.path.isdir(test_tmp_dir):
    os.makedirs(test_tmp_dir)

  discover_args = [
    'python', kludge, 'discover',
    '-I', test_generate_dir,
    '-o', test_tmp_dir,
    basename,
    os.path.join(test_discover_dir, basename + '.hpp'),
    ]
  print 'RUN: ' + ' '.join(discover_args)
  assert subprocess.call(discover_args) == 0

  generate_args = [
    'python', kludge, 'generate',
    '--debug-type-templates',
    basename,
    basename + '.kludge.py',
    ]
  print 'RUN: ' + ' '.join(generate_args)
  assert subprocess.call(
    generate_args,
    cwd = test_tmp_dir,
    ) == 0

  scons_env = os.environ.copy()
  scons_env['CPPPATH'] = root_dir
  if platform.system() == 'Windows':
    scons_args = ['scons.bat']
  else:
    scons_args = ['scons']
  scons_args.extend([
    '-f', basename + '.SConstruct',
    'VERBOSE=1',
    ])
  print 'RUN: ' + ' '.join(scons_args)
  assert subprocess.call(
    scons_args,
    cwd = test_tmp_dir,
    env = scons_env,
    ) == 0
