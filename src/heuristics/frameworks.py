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
