from pydriller import RepositoryMining, ModificationType

from src.delta_analyzer.tasks import *
from src.common import *
from src.heuristics import *

def analyze_commits(repo_url):
  framework_occurrences = {
    'first_unittest': { 'hash': None, 'index': None },
    'last_unittest': { 'hash': None, 'index': None },
    'first_pytest': { 'hash': None, 'index': None },
    'last_pytest': { 'hash': None, 'index': None }
  }

  migration_occurrences = {
    'first': { 'hash': None, 'index': None },
    'last': { 'hash': None, 'index': None }
  }

  allcommits = []
  authors_info = []

  index = 0
  for commit in RepositoryMining(repo_url, only_no_merge=True).traverse_commits():
    memo = __init_memo(index, commit, repo_url)
  
    for modification in commit.modifications:
      if should_analyze(modification):
        source_code, removed_lines, added_lines, path = extract_information(modification)
        memo, framework_occurrences = handle_framework_occurrences(
          memo, source_code, removed_lines, added_lines, path, framework_occurrences
        )

        if is_test_file(path):
          memo = handle_apis_occurrences(memo, removed_lines, added_lines)

    memo, migration_occurrences = \
      handle_tags_and_migrations_occurrence(memo, migration_occurrences, framework_occurrences)
    allcommits.append(memo)
    index += 1
  
  authors_info_by_name, authors_info_by_email = handle_authors_info(allcommits)

  return (
    framework_occurrences,
    migration_occurrences,
    allcommits,
    authors_info_by_name,
    authors_info_by_email
  )

def __init_memo(index, commit, repo_url):
  count_obj = { key: 0 for key in count_columns }
  matches_obj = { key: [] for key in matches_columns }
  references_obj = { key: False for key in references_columns }
  tags_obj = { key: False for key in tags_columns }

  return {
    "commit_index": index,
    "author_email": commit.author.email,
    "author_name": commit.author.name,
    "date": commit.author_date,
    "files_changed": len(commit.modifications),
    "commit_message": commit.msg,
    "commit_hash": commit.hash,
    "commit_link": repo_url + '/commit/' + commit.hash,
    "repo_url": repo_url,
    "are_we_interested": False,
    **references_obj,
    **tags_obj,
    "tags": [],
    **count_obj,
    **matches_obj
  }
