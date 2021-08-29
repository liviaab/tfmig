from src.heuristics.apis_pytest import APIsPytest
from src.common.search_patterns import *

contents = """
import logging
import pytest-mock

import pytest
from docker.errors import APIError

def test_answer():
    assert inc(3) == 5

# XFail: mark test functions as expected to fail
@pytest.mark.xfail(raises=IndexError)
def test_f():
    f()

def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0

def test_function():
    if not valid_config():
        pytest.xfail("failing configuration (but should work)")

xfail = pytest.mark.xfail

@xfail
def test_hello():
    assert 0

@pytest.fixture
def my_fruit():
    return Fruit("apple")

# Using marks with parametrized fixtures
@pytest.fixture(params=[0, 1, pytest.param(2, marks=pytest.mark.skip)])
def data_set(request):
    return request.param

@pytest.mark.usefixtures("cleandir", "anotherfixture")
def test():
    ...

# pytest.param - Specify a parameter in pytest.mark.parametrize calls or parametrized fixtures.
@pytest.mark.parametrize(
    "test_input,expected",
    [("3+5", 8), ("2+4", 6), pytest.param("6*9", 42, marks=pytest.mark.xfail)],
)
def test_eval(test_input, expected):
    assert eval(test_input) == expected

@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_foo(x, y):
    pass


@pytest.mark.skip(reason="no way of currently testing this")
def test_the_unknown():
    ...

def test_function():
    if not valid_config():
        pytest.skip("unsupported configuration")

# Skip all tests in a module based on some condition:
pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="tests for linux only")
""" 

def test_find_the_correct_amount_and_matches_of_apis_in_list_of_lines():
  list_of_contents = contents.split('\n')
  result = search_patterns_in_contents(APIsPytest, list_of_contents)

  expected = {
    "count_native_assert": 3,
    "count_pytest_raises": 1,
    "count_simple_skip": 1,
    "count_mark_skip": 3,
    "count_pytest_expected_failure": 4,
    "count_fixture": 2,
    "count_usefixtures": 1,
    "count_parametrize": 3,
    "count_generic_mark": 10,
    "count_generic_pytest": 8,
    "count_monkeypatch": 0,
    "count_pytest_mock": 1,
    "count_import_pytest": 1,

    "matches_native_assert": ['inc(3) == 5', '0', 'eval(test_input) == expected'],
    "matches_pytest_raises": ['(ZeroDivisionError)'],
    "matches_simple_skip": ['()'],
    "matches_mark_skip": ['', '(reason=)',  'if(sys.platform == )'],
    "matches_pytest_expected_failure": ['(raises=IndexError)', '()', '', ''],
    "matches_fixture": ['', '(params=[0, 1, pytest.param(2, marks=pytest.mark.skip)])'],
    "matches_usefixtures": ['()'],
    "matches_parametrize": ['', '(, [0, 1])', '(, [2, 3])'],
    "matches_generic_mark": [
      'xfail(raises=IndexError)', 
      'xfail', 'skip)])',
      'usefixtures()',
      'parametrize(',
      'xfail)],',
      'parametrize(, [0, 1])',
      'parametrize(, [2, 3])',
      'skip(reason=)',
      'skipif(sys.platform == )'
    ],
    "matches_generic_pytest": [
      'mark.xfail(raises=IndexError)',
      'fixture',
      'fixture(params=[0, 1, pytest.param(2, marks=pytest.mark.skip)])', 
      'mark.usefixtures()',
      'mark.parametrize(',
      'mark.parametrize(, [0, 1])',
      'mark.parametrize(, [2, 3])',
      'mark.skip(reason=)'
    ],
    "matches_monkeypatch": [],
    "matches_pytest_mock": ['pytest-mock'],
    "matches_import_pytest": ['import pytest'],
  }

  assert result == expected

def test_find_the_correct_amount_and_matches_of_apis_in_file():
  with open('tests/fixtures/test_pytest.py', 'r') as file:
    content = file.read()
    result = search_patterns_in_content(APIsPytest, content)
  
    expected = {
      "count_native_assert": 9,
      "count_pytest_raises": 2,
      "count_simple_skip": 2,
      "count_mark_skip": 6,
      "count_pytest_expected_failure": 7,
      "count_fixture": 11,
      "count_usefixtures": 2,
      "count_parametrize": 4,
      "count_generic_mark": 19,
      "count_generic_pytest": 24,
      "count_monkeypatch": 0,
      "count_pytest_mock": 0,
      "count_import_pytest": 1,

      "matches_native_assert": [
        'inc(3) == 5', '0', '0', '0', 'fixt == 42', 'my_fruit in fruit_basket',
        'os.listdir(os.getcwd()) == []', 'os.listdir(os.getcwd()) == []', 
        'eval(test_input) == expected'],
      "matches_pytest_raises": ['(ZeroDivisionError)', '(ValueError, match=r)'],
      "matches_simple_skip": ['()', '(, allow_module_level=True)'],
      "matches_mark_skip": [
        '', '(reason=)', 'if(sys.version_info < (3, 7), reason=)',
        '', '()', 'if(sys.platform == )'
      ],
      "matches_pytest_expected_failure": [
        '(raises=IndexError)', '()', '(sys.platform == )',
       '(run=False)', '(strict=True)', '', ''
      ],
      "matches_fixture": [
        '', '', '(scope=)', '(scope=)', '(autouse=True)', '(scope=])',
        '(params=[0, 1], ids=[])', '(params=[0, 1], ids=idfn)', 
        '(params=[0, 1, pytest.param(2, marks=pytest.mark.skip)])',
        '(scope=])', '(scope=, params=[1, 2])'
      ],
      "matches_usefixtures": ['()', '()'],
      "matches_parametrize": ['(, 42)])', '', '(, [0, 1])', '(, [2, 3])'],
      "matches_generic_mark": [
        'xfail(raises=IndexError)',
        'xfail(sys.platform == )',
        'xfail(run=False)',
        'xfail(strict=True)',
        'xfail',
        'fixt_data(42)',
        'skip)])',
        'usefixtures()',
        'usefixtures()',
        'parametrize(, 42)])',
        'parametrize(',
        'xfail)],',
        'parametrize(, [0, 1])',
        'parametrize(, [2, 3])',
        'skip(reason=)',
        'skipif(sys.version_info < (3, 7), reason=)',
        'skipif(',
        'skip()',
        'skipif(sys.platform == )'
      ],
      "matches_generic_pytest": [
        'mark.xfail(raises=IndexError)',
        'mark.xfail(sys.platform == )',
        'mark.xfail(run=False)',
        'mark.xfail(strict=True)',
        'mark.fixt_data(42)',
        'fixture',
        'fixture',
        'fixture(scope=)',
        'fixture(scope=)',
        'fixture(autouse=True)',
        'fixture(scope=])',
        'fixture(params=[0, 1], ids=[])',
        'fixture(params=[0, 1], ids=idfn)',
        'fixture(params=[0, 1, pytest.param(2, marks=pytest.mark.skip)])',
        'fixture(scope=])',
        'fixture(scope=, params=[1, 2])',
        'mark.usefixtures()',
        'mark.usefixtures()',
        'mark.parametrize(, 42)])',
        'mark.parametrize(',
        'mark.parametrize(, [0, 1])',
        'mark.parametrize(, [2, 3])',
        'mark.skip(reason=)',
        'mark.skipif(sys.version_info < (3, 7), reason=)'
      ],
      "matches_monkeypatch": [],
      "matches_pytest_mock": [],
      "matches_import_pytest": ['import pytest'],
    }

    assert result == expected
