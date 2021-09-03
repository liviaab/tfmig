import os
import csv

from src.delta_analyzer import run
from src.common.csv_utils import *

def test_metrics_generation():
  # setup
  current_dir = os.getcwd()

  path_to_oracles = [ 
    os.path.join(current_dir, 'tests/fixtures/oracles/comment_to_valid_ref_pytest'),
    os.path.join(current_dir, 'tests/fixtures/oracles/pytest_to_unittest'),
    os.path.join(current_dir, 'tests/fixtures/oracles/sc_unittest_to_pytest_multiplecommits'),
    os.path.join(current_dir, 'tests/fixtures/oracles/comment_to_valid_ref_unittest'),
    os.path.join(current_dir, 'tests/fixtures/oracles/sc_pytest'),
    os.path.join(current_dir, 'tests/fixtures/oracles/sc_unittest_to_pytest_singlecommit'),
    os.path.join(current_dir, 'tests/fixtures/oracles/count_pytest_apis'),
    os.path.join(current_dir, 'tests/fixtures/oracles/sc_pytest_config_file'),
    os.path.join(current_dir, 'tests/fixtures/oracles/valid_ref_to_comment_pytest'),
    os.path.join(current_dir, 'tests/fixtures/oracles/count_unittest_apis'),
    os.path.join(current_dir, 'tests/fixtures/oracles/sc_unittest'),
    os.path.join(current_dir, 'tests/fixtures/oracles/valid_ref_to_comment_unittest'),
    os.path.join(current_dir, 'tests/fixtures/oracles/docstring_pytest'),
    os.path.join(current_dir, 'tests/fixtures/oracles/sc_unittest_and_pytest'),
    os.path.join(current_dir, 'tests/fixtures/oracles/docstring_unittest'),
    os.path.join(current_dir, 'tests/fixtures/oracles/sc_unittest_config_file')
  ]

  metrics_filepath = run(path_to_oracles)
  expected_filepath = os.path.join(current_dir, 'tests/fixtures/oracles/000_metrics.csv')

  # testing
  with open(metrics_filepath) as result, open(expected_filepath) as expected:
    reader_result = csv.DictReader(result)
    reader_expected = csv.DictReader(expected)
    assert [ row['Past/Present'] for row in reader_result ] == [  row['Past/Present'] for row in reader_expected ]

  # clean up
  folder = metrics_filepath.replace("000_metrics.csv", "")
  remove_folder(folder)
  return
