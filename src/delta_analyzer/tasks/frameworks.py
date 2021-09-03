from src.common.columns import *
from src.common.search_patterns import *
from src.heuristics.frameworks import *
from src.heuristics.test_file import *

def handle_framework_occurrences(memo, source_code, removed_lines, added_lines, path, framework_occurrences):
  modification_memo ={
    "unittest_in_code": __search_patterns_in_content(UnittestRef, source_code),
    "unittest_in_added_diffs": __search_patterns_in_contents(UnittestRef, added_lines),
    "unittest_in_removed_diffs": __search_patterns_in_contents(UnittestRef, removed_lines, ignoreComments=False),
    "pytest_in_code": __search_patterns_in_content(PytestRef, source_code),
    "pytest_in_added_diffs": __search_patterns_in_contents(PytestRef, added_lines),
    "pytest_in_removed_diffs": __search_patterns_in_contents(PytestRef, removed_lines, ignoreComments=False),
    "has_test_file": __search_patterns_in_content(TestFileRef, path)
  }

  # rules to update references
  if not framework_occurrences['first_unittest']['hash'] and modification_memo["unittest_in_added_diffs"]:
    framework_occurrences['first_unittest']['hash'] = memo['commit_hash']
    framework_occurrences['first_unittest']['index'] = memo['commit_index']

  if framework_occurrences['first_unittest']['hash'] and modification_memo["unittest_in_removed_diffs"]:
    framework_occurrences['last_unittest']['hash'] = memo['commit_hash']
    framework_occurrences['last_unittest']['index'] = memo['commit_index']

  if not framework_occurrences['first_pytest']['hash'] and modification_memo["pytest_in_added_diffs"]:
    framework_occurrences['first_pytest']['hash'] = memo['commit_hash']
    framework_occurrences['first_pytest']['index'] = memo['commit_index']
  
  if framework_occurrences['first_pytest']['hash'] and modification_memo["pytest_in_removed_diffs"]:
    framework_occurrences['last_pytest']['hash'] = memo['commit_hash']
    framework_occurrences['last_pytest']['index'] = memo['commit_index']

  # update memo
  for key in references_columns:
    memo[key] |= modification_memo[key]

  return (memo, framework_occurrences)


def is_test_file(path):
  result = __search_patterns_in_content(TestFileRef, path)
  return result

def __search_patterns_in_content(patterns, content):
  result = search_patterns_in_content(patterns, content)
  key = next( key for key in list(result.keys()) if key.startswith('count_') )
  return result[key] > 0

def __search_patterns_in_contents(patterns, content, ignoreComments=True):
  result = search_patterns_in_contents(patterns, content, ignoreComments) 
  key = next( key for key in list(result.keys()) if key.startswith('count_') )
  return result[key] > 0
