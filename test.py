#!/usr/bin/env python
#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import os, pytest, subprocess, difflib

test_generate_dir = os.path.join('test', 'generate')
test_generate_tmp_dir_base = os.path.join('test', 'tmp', 'generate')

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

@pytest.mark.parametrize("kludge_py_basename", collect_test_generate_basenames())
def test_generate(kludge_py_basename):

  if os.path.isfile(os.path.join(test_generate_dir, kludge_py_basename + '.skip')):
    return

  test_tmp_dir = os.path.join(test_generate_tmp_dir_base, kludge_py_basename)

  if not os.path.isdir(test_tmp_dir):
    os.makedirs(test_tmp_dir)

  assert subprocess.call(
    [
      './kludge', 'generate',
      '-o', test_tmp_dir,
      # '--debug-type-templates',
      kludge_py_basename,
      os.path.join(test_generate_dir, kludge_py_basename + '.kludge.py'),
      ],
    ) == 0

  scons_env = os.environ.copy()
  scons_env['CPPPATH'] = os.path.abspath(test_generate_dir)
  assert subprocess.call(
    [
      'scons',
      '-f', kludge_py_basename + '.SConstruct',
      ],
    cwd = test_tmp_dir,
    env = scons_env,
    ) == 0

  kl_env = os.environ.copy()
  kl_env['FABRIC_EXTS_PATH'] = test_tmp_dir
  with open(os.path.join(test_tmp_dir, kludge_py_basename + '.test.out')) as expected_kl_output_file:
    expected_kl_output = expected_kl_output_file.read().splitlines()
  actual_kl_output = subprocess.check_output(
    [
      'kl',
      os.path.join(test_tmp_dir, kludge_py_basename + '.test.kl'),
      ],
    env = kl_env,
    ).splitlines()
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

  assert subprocess.call(
    [
      './kludge', 'discover',
      '-o', test_tmp_dir,
      os.path.join(test_discover_dir, basename + '.hpp'),
      ],
    ) == 0

  # scons_env = os.environ.copy()
  # scons_env['CPPPATH'] = os.path.abspath(test_discover_dir)
  # assert subprocess.call(
  #   [
  #     'scons',
  #     '-f', kludge_py_basename + '.SConstruct',
  #     ],
  #   cwd = test_tmp_dir,
  #   env = scons_env,
  #   ) == 0

  # kl_env = os.environ.copy()
  # kl_env['FABRIC_EXTS_PATH'] = test_tmp_dir
  # with open(os.path.join(test_tmp_dir, kludge_py_basename + '.test.out')) as expected_kl_output_file:
  #   expected_kl_output = expected_kl_output_file.read().splitlines()
  # actual_kl_output = subprocess.check_output(
  #   [
  #     'kl',
  #     os.path.join(test_tmp_dir, kludge_py_basename + '.test.kl'),
  #     ],
  #   env = kl_env,
  #   ).splitlines()
  # difflines = difflib.unified_diff(expected_kl_output, actual_kl_output)
  # diffline_count = 0
  # for diffline in difflines:
  #   print diffline
  #   diffline_count += 1
  # assert diffline_count == 0
