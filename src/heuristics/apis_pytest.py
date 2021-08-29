# List of regular expressions that will be searched in the diffs (commits)
# If you want to add another expression to be matched, you just need to add
# in this list, following the pattern.

APIsPytest = [
  {
    "name": "native_assert",
    "regex": r"\s*assert\s+(.*)"
  },
  {
    "name": "pytest_raises",
    "regex": r"pytest.raises(\(.*\))"
  },
  {
    "name": "simple_skip",
    "regex": r"pytest.skip(\(.*\))"
  },
  {
    "name": "mark_skip",
    "regex": r"[@]?pytest.mark.skip(.*\(.*\))?"
  },
  {
    "name": "expected_failure",
    "regex": r"[@]?pytest[.mark]*?.[x]*?fail(\(.*\))?"
    # matches pytest.xfail | pytest.fail | @pytest.mark.xfail
  },
  {
    "name": "fixture",
    "regex": r"@pytest.fixture(.*)"
  },
  {
    "name": "usefixtures",
    "regex": r"@pytest.mark.usefixtures(\(.*\))?"
  },
  {
    "name": "parametrize",
    "regex": r"@pytest.mark.parametrize(\(.*\))?"
  },
  {
    "name": "generic_mark",
    "regex": r"[@]?pytest.mark\.(.*)"
  },
  {
    "name": "generic_pytest",
    "regex": r"@pytest\.(.*)"
  },
  {
    "name": "monkeypatch",
    "regex": r"\s*monkeypatch\.(.*)"
  },
  {
    "name": "pytest_mock",
    "regex": r"(pytest-mock)"
  },
  {
    "name": "import_pytest",
    "regex": r"(import\s+pytest(?!-mock))"
  }
]
