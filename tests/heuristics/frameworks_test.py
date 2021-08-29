from src.heuristics.frameworks import UnittestRef, PytestRef
from src.common.search_patterns import *

contents_unittest = """import unittest
import unittest-mock
import unittest.mock
from unittest import Mock

unittests


import unittest"""

contents_pytest = """import pytest
import pytest-mock

import pytest"""

def test_pytest_heuristic_in_list_of_pytest_contents():
  lines = contents_pytest.split('\n')
  result = search_patterns_in_contents(PytestRef, lines)
  expected = {
    'count_pytest_reference': 2,
    'matches_pytest_reference': [('pytest', ''), ('pytest', '')]
  }
  assert expected == result

def test_pytest_heuristic_in_list_of_unittest_contents():
  lines = contents_unittest.split('\n')
  result = search_patterns_in_contents(PytestRef, lines)
  expected = {
    'count_pytest_reference': 0,
    'matches_pytest_reference': []
  }
  assert expected == result

def test_unittest_heuristic_in_list_of_pytest_contents():
  lines = contents_pytest.split('\n')
  result = search_patterns_in_contents(UnittestRef, lines)
  expected = {
    'count_unittest_reference': 0,
    'matches_unittest_reference': []
  }
  assert expected == result

def test_unittest_heuristic_in_list_of_unittest_contents():
  lines = contents_unittest.split('\n')
  result = search_patterns_in_contents(UnittestRef, lines)
  expected = {
    'count_unittest_reference': 2,
    'matches_unittest_reference': [('unittest', ''), ('unittest', '')]
  }
  assert expected == result

def test_pytest_heuristic_in_pytest_file():
  with open('tests/fixtures/test_pytest.py', 'r') as file:
    content = file.read()
    result = search_patterns_in_content(PytestRef, content)
    assert result['count_pytest_reference'] == 37

def test_unittest_heuristic_in_pytest_file():
  with open('tests/fixtures/test_pytest.py', 'r') as file:
    content = file.read()
    result = search_patterns_in_content(UnittestRef, content)
    expected = {
      'count_unittest_reference': 0,
      'matches_unittest_reference': []
    }
    assert expected == result

def test_pytest_heuristic_in_unittest_file():
  with open('tests/fixtures/test_unittest.py', 'r') as file:    
    content = file.read()
    result = search_patterns_in_content(PytestRef, content)
    expected = {
      'count_pytest_reference': 0,
      'matches_pytest_reference': []
    }
    assert expected == result

def test_unittest_heuristic_in_unittest_file():
  with open('tests/fixtures/test_unittest.py', 'r') as file:    
    content = file.read()
    result = search_patterns_in_content(UnittestRef, content)
    assert result['count_unittest_reference'] == 11


def test_both_heuristics_in_mixed_file():
  with open('tests/fixtures/test_both.py', 'r') as file:
    content = file.read()
    result = search_patterns_in_content(UnittestRef, content)
    assert result['count_unittest_reference'] == 11

    result = search_patterns_in_content(PytestRef, content)
    assert result['count_pytest_reference'] == 1


def test_pytest_heuristic_in_ci_pytest_file():
  with open('tests/fixtures/integration_pytest.yml', 'r') as file:
    content = file.read()
    result = search_patterns_in_content(PytestRef, content)
    assert result['count_pytest_reference'] == 3

def test_unittest_heuristic_in_ci_unittest_file():
  with open('tests/fixtures/integration_unittest.yaml', 'r') as file:
    content = file.read()
    result = search_patterns_in_content(UnittestRef, content)
    assert result['count_unittest_reference'] == 2

def test_both_heuristics_in_ci_mixed_file():
  with open('tests/fixtures/integration_both.yaml', 'r') as file:
    content = file.read()
    result = search_patterns_in_content(UnittestRef, content)
    assert result['count_unittest_reference'] == 2

    result = search_patterns_in_content(PytestRef, content)
    assert result['count_pytest_reference'] == 3

