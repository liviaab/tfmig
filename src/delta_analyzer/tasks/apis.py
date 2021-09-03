from src.common.search_patterns import *
from src.heuristics import APIsPytest, APIsUnittest

def handle_apis_occurrences(memo, removed_lines, added_lines):
  u_apis_in_added_lines = search_patterns_in_contents(APIsUnittest, added_lines)
  u_apis_in_removed_lines = search_patterns_in_contents(APIsUnittest, removed_lines)
  p_apis_in_added_lines = search_patterns_in_contents(APIsPytest, added_lines)
  p_apis_in_removed_lines = search_patterns_in_contents(APIsPytest, removed_lines)

  u_apis_in_added_lines = { 'u_added_'+key: value for key, value in u_apis_in_added_lines.items() }
  u_apis_in_removed_lines = { 'u_removed_'+key: value for key, value in u_apis_in_removed_lines.items() }
  p_apis_in_added_lines = { 'p_added_'+key: value for key, value in p_apis_in_added_lines.items() }
  p_apis_in_removed_lines = { 'p_removed_'+key: value for key, value in p_apis_in_removed_lines.items() }

  modification_memo = {
    **u_apis_in_added_lines,
    **u_apis_in_removed_lines,
    **p_apis_in_added_lines,
    **p_apis_in_removed_lines,
  }

  for key in modification_memo.keys():
    memo[key] += modification_memo[key]

  return memo
