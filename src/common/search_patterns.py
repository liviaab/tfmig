import re
from pyparsing import Regex, pythonStyleComment, dblQuotedString, sglQuotedString, quotedString
from src.common.docstring_pattern import docString

DJANGO_DOCTEST_COMMENT = 'This file demonstrates writing tests using the unittest module. These will pass'

# Function search_patterns_in_contents
# param patterns      list of objects with `name` and `regex` keys. E. g.:
#                     [
#                         {
#                             "name": "native_assert"
#                             "regex": "\s*assert\s+(.*)"
#                         },
#                         {
#                             "name": "pytest_raises"
#                             "regex": "pytest.raises(\(.*\))"
#                         }
#                     ]

# param contents     list of strings where the patterns will be matched
def search_patterns_in_contents(patterns, contents, ignoreComments=True):
  result = __init_result(patterns)

  for content in contents:
    if content.strip() == '' or content.strip().startswith('"""') or content == DJANGO_DOCTEST_COMMENT:
      continue

    if ignoreComments and content.strip().startswith('#'):
      continue

    tmp_result = search_patterns_in_content(patterns, content, ignoreComments)
    for key, value in tmp_result.items():
      result[key] += value

  return result

# Function search_patterns_in_content
# param patterns      list of objects with `name` and `regex` keys. E. g.:
#                     [
#                         {
#                             "name": "native_assert"
#                             "regex": "\s*assert\s+(.*)"
#                         },
#                         {
#                             "name": "pytest_raises"
#                             "regex": "pytest.raises(\(.*\))"
#                         }
#                     ]

# param contents     string (or file content) where the patterns will be matched
def search_patterns_in_content(patterns, content, ignoreComments=True):
  result = __init_result(patterns)

  if content == None:
    return result

  expr = Regex(r'.*')
  if ignoreComments:
    expr = Regex(r'.*').ignore(pythonStyleComment | quotedString | dblQuotedString | sglQuotedString | docString)

  filtered_result = list(expr.scanString(content))
  # remove strings from code
  filtered_result = [ re.sub("[\"|\'](.*)[\"|\']", "", text[0]) for (text, a, b) in filtered_result]
  # remove comments that starts at the middle/are in the end of the line
  filtered_result = '\n'.join([ re.sub("[\#](.*)", "", line) for line in filtered_result])

  for pattern in patterns: 
    count_key = 'count_' + pattern['name']
    matches_key = 'matches_' + pattern['name'] 

    matches = re.findall(pattern['regex'], filtered_result)
    result[count_key] = len(matches)
    result[matches_key] = matches

  return result

def __init_result(patterns):
  result = {}

  for pattern in patterns:
    count_key = 'count_' + pattern['name']
    matches_key = 'matches_' + pattern['name']
    result = {
        **result, 
        **{
          count_key: 0,
          matches_key: []
        }
      }
  return result

