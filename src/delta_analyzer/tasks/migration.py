from src.common.columns import *

def handle_tags_and_migrations_occurrence(memo, migration_occurrences, framework_occurrences):
  memo = __update_migration_tags(memo, framework_occurrences)
  migration_occurrences = __update_migration_occurrences(memo, migration_occurrences)

  return (memo, migration_occurrences)


def __update_migration_tags(memo, framework_occurrences):
  if __migrates_asserts(memo, framework_occurrences):
      memo["tags"].append("assert_migration")
      memo["Mig: assert"] = True

  if __migrates_fixtures(memo, framework_occurrences):
      memo["tags"].append("fixture_migration")
      memo["Mig: fixture"] = True

  if __migrates_frameworks(memo, framework_occurrences):
      memo["tags"].append("framework_migration")
      memo["Mig: import"] = True

  if __migrates_skips(memo, framework_occurrences):
      memo["tags"].append("skip_migration")
      memo["Mig: skip"] = True

  if __migrates_expected_failure(memo, framework_occurrences):
      memo["tags"].append("expected_failure_migration")
      memo["Mig: failure"] = True

  if (memo["tags"] != []):
      memo["are_we_interested"] = True

      # "extra" tags
      if __adds_parametrized_test(memo, framework_occurrences):
          memo["tags"].append("adds_parametrized_test")
          memo["Mig: add Param"] = True

      if __migrates_testcase(memo, framework_occurrences):
          memo["tags"].append("testcase_migration")
          memo["Mig: testcase"] = True
  
  return memo

def __update_migration_occurrences(memo, migration_occurrences):
  if not memo['are_we_interested']:
    return migration_occurrences

  if not migration_occurrences['first']['hash']:
    migration_occurrences['first']['hash'] = memo['commit_hash']
  migration_occurrences['first']['index'] = memo['commit_index']
  
  if migration_occurrences['first']['hash']:
    migration_occurrences['last']['hash'] = memo['commit_hash']
    migration_occurrences['last']['index'] = memo['commit_index']
  
  return migration_occurrences

def __migrates_asserts(memo, framework_occurrences):
    return framework_occurrences['first_unittest']['hash'] and \
            framework_occurrences['first_pytest']['hash'] and \
            memo["u_added_count_self_assert"] == 0 and \
            memo["u_removed_count_self_assert"] > 0 and \
            memo["p_added_count_native_assert"] > 0 and \
            memo["p_removed_count_native_assert"] == 0

def __migrates_skips(memo, framework_occurrences):
    return framework_occurrences['first_unittest']['hash'] and \
            framework_occurrences['first_pytest']['hash'] and \
            (memo["u_added_count_unittest_self_skip"] == 0 and memo["u_added_count_unittest_skip"] == 0 ) and \
            (memo["u_removed_count_unittest_self_skip"] > 0 or memo["u_removed_count_unittest_skip"] > 0 ) and \
            (memo["p_removed_count_simple_skip"] == 0 and memo["p_removed_count_mark_skip"] == 0) and \
            (memo["p_added_count_simple_skip"] > 0 or memo["p_added_count_mark_skip"] > 0)

def __migrates_expected_failure(memo, framework_occurrences):
    return framework_occurrences['first_unittest']['hash'] and \
            framework_occurrences['first_pytest']['hash'] and \
            (memo["u_added_count_unittest_expected_failure"] == 0) and \
            (memo["u_removed_count_unittest_expected_failure"] > 0) and \
            (memo["p_added_count_pytest_expected_failure"] > 0) and \
            (memo["p_removed_count_pytest_expected_failure"] == 0)


def __migrates_fixtures(memo, framework_occurrences):
    return framework_occurrences['first_unittest']['hash'] and \
            framework_occurrences['first_pytest']['hash'] and \
            (memo["u_added_count_setup"] == 0 and memo["u_added_count_setupClass"] == 0 and \
              memo["u_added_count_teardown"] == 0 and memo["u_added_count_teardownClass"] == 0) and \
            (memo["u_removed_count_setup"] > 0 or memo["u_removed_count_setupClass"] > 0 or \
              memo["u_removed_count_teardown"] > 0 or memo["u_removed_count_teardownClass"] > 0) and \
            (memo["p_added_count_fixture"] > 0 or memo["p_added_count_usefixtures"] > 0) and \
            (memo["p_removed_count_fixture"] == 0 and memo["p_removed_count_usefixtures"] == 0)

def __migrates_frameworks(memo, framework_occurrences):
    return framework_occurrences['first_unittest']['hash'] and \
            framework_occurrences['first_pytest']['hash'] and \
            memo["u_added_count_import_unittest"] == 0 and \
            memo["u_removed_count_import_unittest"] > 0 and \
            memo["p_removed_count_import_pytest"] == 0 and \
            memo["p_added_count_import_pytest"] > 0

def __migrates_testcase(memo, framework_occurrences):
    return framework_occurrences['first_unittest']['hash'] and \
            framework_occurrences['first_pytest']['hash'] and \
            memo["u_removed_count_testcase_subclass"] > 0 and \
            memo["u_added_count_testcase_subclass"] == 0

def __adds_parametrized_test(memo, framework_occurrences):
    return framework_occurrences['first_unittest']['hash'] and \
            framework_occurrences['first_pytest']['hash'] and \
            memo["p_added_count_parametrize"] > 0 and \
            memo["p_removed_count_parametrize"] == 0
