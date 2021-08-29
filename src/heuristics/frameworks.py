# List of regular expressions that will be searched in the diffs (commits)
# If you want to add another expression to be matched, you just need to add
# in this list, following the pattern.

UnittestRef =  [
    {
    "name": "unittest_reference",
    "regex": r"(unittest(\Z|\s+|\W|\b)(?!.*[m|M]ock))"
  }
]

PytestRef = [
    {
    "name": "pytest_reference",
    "regex": r"(pytest(\Z|\s+|\W)(?!mock))"
  }
]
