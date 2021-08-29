import re
from pyparsing import Regex, pythonStyleComment, dblQuotedString, sglQuotedString, quotedString
from src.common.docstring_pattern import docString

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
def search_patterns_in_contents(patterns, contents):
  result = __init_result(patterns)

  for content in contents:
    if content.strip().startswith('#') or content.strip() == '' or content.strip().startswith('"""'):
      continue

    tmp_result = search_patterns_in_content(patterns, content)
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
def search_patterns_in_content(patterns, content, ignoreStrings=True):
  result = __init_result(patterns)

  if content == None:
    return result

  expr = Regex(r'.*').ignore(pythonStyleComment | quotedString | dblQuotedString | sglQuotedString | docString)
  filtered_result = list(expr.scanString(content))
  filtered_result = '\n'.join([ re.sub("[\"|\'](.*)[\"|\']", "", text[0]) for (text, _, _ ) in filtered_result])

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

