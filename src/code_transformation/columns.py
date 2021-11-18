output_columns = [
  "Transformation type",
  "First - commit count",
  "25% - commit count",
  "50% - commit count",
  "75% - commit count",
  "100% - commit count",

  "First - code transformation",
  "25% - code transformation",
  "50% - code transformation",
  "75% - code transformation",
  "100% - code transformation",

  "total unittest removals",
  "total pytest additions"
]

assert_columns = {
  "u_removal": ["u_removed_count_self_assert"],
  "p_addition": ["p_added_count_native_assert"]
}

fixture_columns = {
  "u_removal": ["u_removed_count_setup",	"u_removed_count_setupClass",	"u_removed_count_teardown",	"u_removed_count_teardownClass"],
  "p_addition": ["p_added_count_fixture",	"p_added_count_usefixtures"]
}

import_columns = {
  "u_removal": ["u_removed_count_import_unittest"],
  "p_addition": ["p_added_count_import_pytest"]
}

skip_columns = {
  "u_removal": ["u_removed_count_unittest_skip",	"u_removed_count_unittest_self_skip"],
  "p_addition": ["p_added_count_simple_skip",	"p_added_count_mark_skip"]
}

failure_columns = {
  "u_removal": ["u_removed_count_unittest_expected_failure"],
  "p_addition": ["p_added_count_pytest_expected_failure"]
}

transformation_columns_by_type = {
  "Mig: assert": assert_columns,
  "Mig: fixture": fixture_columns,
  "Mig: import": import_columns,
  "Mig: skip": skip_columns,
  "Mig: failure": failure_columns
}
