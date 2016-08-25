#!/usr/bin/env python
#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import os, pytest, subprocess, difflib

test_gen_dir = os.path.join('test', 'gen')
test_tmp_dir_base = os.path.join('test', 'tmp')

def collect_test_gen_kludge_py_basenames():
  result = []
  for dirpath, _subdirs, filenames in os.walk(test_gen_dir):
      for filename in filenames:
          filebase_and_ext2, fileext1 = os.path.splitext(filename)
          if fileext1 == '.py':
            filebase, fileext2 = os.path.splitext(filebase_and_ext2)
            if fileext2 == '.kludge':
                result.append(filebase)
  return result

@pytest.mark.parametrize("kludge_py_basename", collect_test_gen_kludge_py_basenames())
def test_kludge_py_basename(kludge_py_basename):

  test_tmp_dir = os.path.join(test_tmp_dir_base, kludge_py_basename)
  
  if not os.path.isdir(test_tmp_dir):
    os.makedirs(test_tmp_dir)

  with open(os.devnull, 'w') as devnull:

    assert subprocess.call(
      [
        './kludge', 'gen',
        '-o', test_tmp_dir,
        kludge_py_basename,
        os.path.join(test_gen_dir, kludge_py_basename + '.kludge.py'),
        ],
      stdout = devnull,
      stderr = devnull,
      ) == 0

    scons_env = os.environ.copy()
    scons_env['CPPPATH'] = os.path.abspath(test_gen_dir)
    assert subprocess.call(
      [
        'scons',
        '-f', kludge_py_basename + '.SConstruct',
        ],
      stdout = devnull,
      stderr = devnull,
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
      stderr = devnull,
      env = kl_env,
      ).splitlines()
    difflines = difflib.unified_diff(expected_kl_output, actual_kl_output)
    diffline_count = 0
    for diffline in difflines:
      print diffline
      diffline_count += 1
    assert diffline_count == 0
