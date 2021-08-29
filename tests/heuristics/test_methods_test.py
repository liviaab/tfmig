from src.heuristics.test_methods import TestMethodRef
from src.common.search_patterns import *

def test_count_test_methods_in_unittest_file():
  with open('tests/fixtures/test_unittest.py', 'r') as file:    
    content = file.read()
    result = search_patterns_in_content(TestMethodRef, content)
    print(result)
  assert result['count_test_methods'] == 12

def test_count_test_methods_in_pytest_file():
  with open('tests/fixtures/test_pytest.py', 'r') as file:    
    content = file.read()
    result = search_patterns_in_content(TestMethodRef, content)
  assert result['count_test_methods'] == 25


def test_count_test_methods_in_mixed_file():
  with open('tests/fixtures/test_both.py', 'r') as file:
    content = file.read()
    result = search_patterns_in_content(TestMethodRef, content)
  assert result['count_test_methods'] == 14


