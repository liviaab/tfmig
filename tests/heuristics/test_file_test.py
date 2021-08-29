from src.heuristics.test_file import TestFileRef
from src.common.search_patterns import *

def test_pattern_in_both_folder_and_file(): 
  result = search_patterns_in_content(TestFileRef, 'tests/apis_pytest_test.py')
  assert result['count_test_file'] == 1

def test_pattern_in_folder(): 
  result = search_patterns_in_content(TestFileRef, 'tests/apis_pytest.py')
  assert result['count_test_file'] == 1

def test_pattern_in_file_suffix(): 
  result = search_patterns_in_content(TestFileRef, 'foo/apis_pytest_test.py')
  assert result['count_test_file'] == 1

def test_pattern_in_file_prefix(): 
  result = search_patterns_in_content(TestFileRef, 'bar/test_foo.py')
  assert result['count_test_file'] == 1

def test_pattern_not_in_filepath(): 
  result = search_patterns_in_content(TestFileRef, 'foo/bar/file.py')
  assert result['count_test_file'] == 0

def test_not_test_entension(): 
  result = search_patterns_in_content(TestFileRef, 'not/python_test.rst')
  assert result['count_test_file'] == 0

