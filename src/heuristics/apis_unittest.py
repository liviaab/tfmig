# List of regular expressions that will be searched in the diffs (commits)
# If you want to add another expression to be matched, you just need to add
# in this list, following the pattern.

APIsUnittest = [
  {
    "name": "testcase_subclass",
    "regex": r"(class\s+.*\([unittest\.]*TestCase.*\):)"
  },
  {
    "name": "self_assert",
    "regex": r"self.assert(\w*)(.*)"
  },
  {
    "name": "setup",
    "regex": r"def\s+setUp\(.*\):"
  },
  {
    "name": "setupClass",
    "regex": r"def\s+setUp(\w+)(\(.*\)):" # setUpClass | setUpModule
  },
  {
    "name": "teardown",
    "regex": r"def\s+tearDown\(.*\):"
  },
  {
    "name": "teardownClass",
    "regex": r"def\s+tearDown(\w+)(\(.*\)):" # tearDownClass | tearDownModule
  },
  {
    "name": "unittest_skip",
    "regex": r"[@]{0,1}unittest.skip.*?\((.*)" # @unittest.skip | @unittest.skipIf | @unittest.skipUnless
  },
  {
    "name": "unittest_self_skip",
    "regex": r"[self.s|unittest.S]kipTest(\(.*)" # self.skipTest() | unittest.SkipTest()
  },
  {
    "name": "unittest_expected_dailure",
    "regex": r"@unittest.expectedFailure"
  },
  {
    "name": "unittest_mock_pattern",
    "regex": r"(\s+unittest.mock\s+|from\s+unittest\s+import\s+mock)"
  },
  {
    "name": "import_unittest",
    "regex": r"(import\s+unittest)"
  }
]
