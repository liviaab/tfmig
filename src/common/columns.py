from src.heuristics import *

# helper method
def create_columns(list_of_dicts, prefix=''):
  columns = []
  for item in list_of_dicts:
    columns.append(prefix + item["name"])

  return columns

# csv metrics per category
repositories_columns = [
  'Past/Present',
  'Repository Name',
  'Repository Link',
  'No. Total Commits',
  'Lifetime in days',

  "No. Commits since 1st unittest occurrence",
  "No. Commits since 1st pytest occurrence",
  'Days since 1st unittest occurrence',
  'Days since 1st pytest occurrence',
  'Days since 1st pytest to last unittest occurrence',

  'No. Authors (name)',
  'No. Migration Authors (name)',
  'No. Authors (email)',
  'No. Migration Authors (email)',
  'No. Authors (email - name)',

  'No. Days (between migration commits)',
  'No. Migration commits',
  'No. Commits (between migration period)',
  'One Commit Migration?',

  'No. Files (current state)',
  'No. Files with unittest',
  'No. Files with pytest',
  'No. Files with both',
  'Pytest before Unittest?',

  '1st commit UNITTEST',
  '1st commit UNITTEST_LINK',
  '1st commit PYTEST',
  '1st commit PYTEST_LINK',

  'Last commit UNITTEST',
  'Last commit UNITTEST_LINK',
  'Last commit PYTEST',
  'Last commit PYTEST_LINK',

  '1st migration commit',
  '1st migration commit link',
  'Last migration commit',
  'Last migration commit link'
]

# csv migration commit
common_columns = [
  "commit_index",
  "author_name",
  "author_email",
  "date",
  "commit_hash",
  "commit_link",
  "commit_message",
  "files_changed",
  "are_we_interested",
]

references_columns = [
  "has_test_file",
  "unittest_in_code",
  "unittest_in_added_diffs",
  "unittest_in_removed_diffs",
  "pytest_in_code",
  "pytest_in_added_diffs",
  "pytest_in_removed_diffs",
]

count_columns = create_columns(APIsUnittest, 'u_added_count_') + create_columns(APIsUnittest, 'u_removed_count_') +\
  create_columns(APIsPytest, 'p_added_count_') + create_columns(APIsPytest, 'p_removed_count_')

matches_columns = create_columns(APIsUnittest, 'u_added_matches_') + create_columns(APIsUnittest, 'u_removed_matches_') +\
  create_columns(APIsPytest, 'p_added_matches_') + create_columns(APIsPytest, 'p_removed_matches_')

tags_columns = [
  "Mig: assert",
  "Mig: fixture",
  "Mig: import",
  "Mig: skip",
  "Mig: failure",
  "Mig: testcase",
  "Mig: add Param",
  "tags"
]

commit_columns = common_columns + references_columns + tags_columns + count_columns + matches_columns

# csv authors
author_columns = [
  "email",
  "total_commits",
  "migration_contributor",
  "migration_commits"
]


