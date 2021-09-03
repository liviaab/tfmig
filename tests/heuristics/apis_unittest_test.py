from src.heuristics.apis_unittest import APIsUnittest
from src.common.search_patterns import *

contents = """import logging
import unittest
from unittest import mock
from unittest.mock import call

from docker.errors import APIError

class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


class DefaultWidgetSizeTestCase(unittest.TestCase):
    # setUpClass is called with the class as the only argument and must be decorated as a classmethod():
    @classmethod
    def setUpClass(cls):
        pass

    # same for tearDownClass
    @classmethod
    def tearDownClass(cls):
        pass

    def setUpModule():
        createConnection()

    def tearDownModule():
        closeConnection()

    def setUp(self):
        self.widget = Widget('The widget')

    def tearDown(self):
        self.widget.dispose()

    def test_default_widget_size(self):
        self.assertEqual(self.widget.size(), (50,50),
                         'incorrect default size')
"""

def test_find_the_correct_amount_and_matches_of_apis_in_list_of_lines():
  list_of_contents = contents.split('\n')
  result = search_patterns_in_contents(APIsUnittest, list_of_contents)

  expected = {
      'count_testcase_subclass': 2,
      'count_self_assert': 5,
      'count_setup': 1,
      'count_setupClass': 2,
      'count_teardown': 1,
      'count_teardownClass': 2,
      'count_unittest_skip': 0,
      'count_unittest_self_skip': 0,
      'count_unittest_expected_failure': 0,
      'count_unittest_mock_pattern': 2,
      'count_import_unittest': 1,

      'matches_testcase_subclass': [
        'class TestStringMethods(unittest.TestCase):',
        'class DefaultWidgetSizeTestCase(unittest.TestCase):'
      ],
      'matches_self_assert': [
        ('Equal', '()'), ('False', '(.isupper())'),
        ('Equal', '(s.split(), [])'), ('Raises', '(TypeError):'),
        ('Equal', '(self.widget.size(), (50,50),')
      ],
      'matches_setup': ['def setUp(self):'],
      'matches_setupClass': [('Class', '(cls)'), ('Module', '()')],
      'matches_teardown': ['def tearDown(self):'],
      'matches_teardownClass': [('Class', '(cls)'), ('Module', '()')],
      'matches_unittest_skip': [],
      'matches_unittest_self_skip': [],
      'matches_unittest_expected_failure': [],
      'matches_unittest_mock_pattern': ['from unittest import mock', ' unittest.mock '],
      'matches_import_unittest': ['import unittest']
  }
  assert expected == result

def test_find_the_correct_amount_and_matches_of_apis_in_file():
  with open('tests/fixtures/test_unittest.py', 'r') as file:
    content = file.read()
    result = search_patterns_in_content(APIsUnittest, content)

  expected = {
    'count_testcase_subclass': 4,
    'count_self_assert': 8,
    'count_setup': 2,
    'count_setupClass': 2,
    'count_teardown': 2,
    'count_teardownClass': 2,
    'count_unittest_skip': 4,
    'count_unittest_self_skip': 1,
    'count_unittest_expected_failure': 1,
    'count_unittest_mock_pattern': 2,
    'count_import_unittest': 1,

    'matches_testcase_subclass': [
      'class TestStringMethods(unittest.TestCase):',
      'class DefaultWidgetSizeTestCase(unittest.TestCase):',
      'class MySkippedTestCase(unittest.TestCase):',
      'class ExpectedFailureTestCase(unittest.TestCase):'
    ],
    'matches_self_assert': [
      ('Equal', '()'), ('False', '(.isupper())'), ('Equal', '(s.split(), [])'),
      ('Raises', '(TypeError):'), ('Equal', '(self.widget.size(), (50,50),'),
      ('Equal', '(self.widget.size(), (100,150),'), ('Equal', '(1, 0, )'),
      ('Equal', '(response.status_code, 200)')
    ],
    'matches_setup': ['def setUp(self):', 'def setUp(self):'],
    'matches_setupClass': [('Class', '(cls)'), ('Module', '()')],
    'matches_teardown': ['def tearDown(self):', 'def tearDown(self):'],
    'matches_teardownClass': [('Class', '(cls)'), ('Module', '()')],
    'matches_unittest_skip': [
      ')', 'mylib.__version__ < (1, 3),', 'sys.platform.startswith()', '.format(obj, attr))'
    ],
    'matches_unittest_self_skip': ['()'],
    'matches_unittest_expected_failure': ['@unittest.expectedFailure'],
    'matches_unittest_mock_pattern': ['from unittest import mock', ' unittest.mock '],
    'matches_import_unittest': ['import unittest']
  }

  assert expected == result
