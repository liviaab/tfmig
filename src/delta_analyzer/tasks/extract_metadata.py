from datetime import datetime, timezone

from src.current_analyzer import *
from src.delta_analyzer.tasks.description import *

def extract_metadata(framework_occurrences, migration_occurrences, allcommits, authors_info_by_name, authors_info_by_email):
  repo_url = allcommits[0]['repo_url']
  (
    total_files,
    unittest_files, 
    pytest_files,
    both_files
  ) = analyze_current(repo_url)

  has_unittest_reference = unittest_files > 0
  has_pytest_reference = pytest_files > 0
  description = get_description_by(framework_occurrences, has_pytest_reference, has_unittest_reference)

  metadata = {
    'Past/Present': description,
    'Repository Name': repo_url.split('/')[-1],
    'Repository Link': repo_url,
    'No. Total Commits': len(allcommits),
    'Lifetime in days': __calculate_time_since(allcommits[0]),

    "No. Commits since 1st unittest occurrence": __calculate_commits_since_first_unittest(framework_occurrences, allcommits),
    "No. Commits since 1st pytest occurrence": __calculate_commits_since_first_pytest(framework_occurrences, allcommits),
    'Days since 1st unittest occurrence': __calculate_time_since_first_unittest(framework_occurrences, allcommits),
    'Days since 1st pytest occurrence': __calculate_time_since_first_pytest(framework_occurrences, allcommits),
    'Days since 1st pytest to last unittest occurrence': __calculate_migration_time(framework_occurrences, allcommits),

    'No. Authors (name)': len(authors_info_by_name),
    'No. Migration Authors (name)': len([ author for author in authors_info_by_name if author["migration_contributor"] ]),
    'No. Authors (email)': len(authors_info_by_email),
    'No. Migration Authors (email)': len([ author for author in authors_info_by_email if author["migration_contributor"] ]),
    'No. Authors (email - name)': len(authors_info_by_email) - len(authors_info_by_name),

    'No. Days (between migration commits)': __calculate_days_between_migration_commits(migration_occurrences, allcommits),
    'No. Migration commits': len([ commit for commit in allcommits if commit["are_we_interested"] ]),
    'No. Commits (between migration period)': __calculate_commits_between_migration_commits(migration_occurrences, allcommits),
    'One Commit Migration?': __check_one_commit_migration(framework_occurrences),

    'No. Files (current state)': total_files,
    'No. Files with unittest': unittest_files,
    'No. Files with pytest': pytest_files,
    'No. Files with both': both_files,
    'Pytest before Unittest?': __pytest_before_unittest(framework_occurrences),

    '1st commit UNITTEST': framework_occurrences['first_unittest']['hash'],
    '1st commit UNITTEST_LINK': __build_occurrence_link(repo_url, framework_occurrences, 'first_unittest'),
    '1st commit PYTEST': framework_occurrences['first_pytest']['hash'],
    '1st commit PYTEST_LINK': __build_occurrence_link(repo_url, framework_occurrences, 'first_pytest'),

    'Last commit UNITTEST': framework_occurrences['last_unittest']['hash'],
    'Last commit UNITTEST_LINK': __build_occurrence_link(repo_url, framework_occurrences, 'last_unittest'),
    'Last commit PYTEST': framework_occurrences['last_pytest']['hash'],
    'Last commit PYTEST_LINK': __build_occurrence_link(repo_url, framework_occurrences, 'last_pytest'),

    '1st migration commit': migration_occurrences['first']['hash'],
    '1st migration commit link': __build_occurrence_link(repo_url, migration_occurrences, 'first'),
    'Last migration commit': migration_occurrences['last']['hash'],
    'Last migration commit link': __build_occurrence_link(repo_url, migration_occurrences, 'last')
  }

  return metadata

def __calculate_commits_since_first_unittest(framework_occurrences, allcommits):
  u_index = framework_occurrences['first_unittest']['index']
  if u_index == None:
    return 0

  return allcommits[-1]["commit_index"] - u_index + 1

def __calculate_commits_since_first_pytest(framework_occurrences, allcommits):
  p_index = framework_occurrences['first_pytest']['index']
  if p_index == None:
    return 0

  return allcommits[-1]["commit_index"] - p_index + 1

def __calculate_time_since(commit):
  timedelta = datetime.now(timezone.utc) - commit['date']
  return timedelta.days

def __calculate_time_since_first_unittest(framework_occurrences, allcommits):
  index = framework_occurrences['first_unittest']['index']
  if index == None:
    return 0

  return __calculate_time_since(allcommits[index])

def __calculate_time_since_first_pytest(framework_occurrences, allcommits):
  index = framework_occurrences['first_pytest']['index']
  if index == None:
    return 0

  return __calculate_time_since(allcommits[index])

def __calculate_migration_time(framework_occurrences, allcommits):
  # Days since 1st pytest to last unittest occurrence
  p_first_index = framework_occurrences['first_pytest']['index']
  u_last_index = framework_occurrences['last_unittest']['index']

  if p_first_index != None and u_last_index != None:
    timedelta = allcommits[p_first_index]['date'] - allcommits[u_last_index]['date']
    return timedelta.days

  return None

def __calculate_days_between_migration_commits(migration_occurrences, allcommits):
  first_index = migration_occurrences['first']['index']
  if first_index == None:
    return 0
  
  last_index = migration_occurrences['last']['index']
  timedelta = allcommits[last_index]['date'] - allcommits[first_index]['date']
  return timedelta.days

def __calculate_commits_between_migration_commits(migration_occurrences, allcommits):
  first_index = migration_occurrences['first']['index']
  if first_index == None:
    return 0
  
  last_index = migration_occurrences['last']['index']
  return last_index - first_index + 1

def __pytest_before_unittest(framework_occurrences):
  if framework_occurrences['first_pytest']['index'] != None and \
      framework_occurrences['first_unittest']['index'] != None and \
      framework_occurrences['first_pytest']['index'] < framework_occurrences['first_unittest']['index']:
    return True
  
  return False

def __check_one_commit_migration(framework_occurrences):
  last_unittest_index = framework_occurrences['last_unittest']['index']
  first_pytest_index = framework_occurrences['first_pytest']['index']

  if last_unittest_index != None and first_pytest_index  != None\
    and (last_unittest_index == first_pytest_index):
    return True

  return False

def __build_occurrence_link(repo_url, occurrence, main_key):
  commit_hash = occurrence[main_key]['hash']
  if commit_hash != None:
    return repo_url + '/commit/' + commit_hash
  
  return None
