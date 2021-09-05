import os
from pydriller import ModificationType

from src.common.extensions import VALID_EXTENSIONS

def should_analyze(modification):
  # should be analyzed if it has a valid extension
  filename, extension = os.path.splitext(modification.filename)
  clause_one = extension in VALID_EXTENSIONS

  # and if it has a valid modification type
  clause_two = modification.change_type in [
    ModificationType.DELETE,
    ModificationType.ADD,
    ModificationType.MODIFY,
    ModificationType.RENAME
  ]
  return clause_one and clause_two

def extract_information(modification):
  source_code = modification.source_code
  removed_lines = []
  added_lines = []
  path = None

  if modification.change_type == ModificationType.DELETE:
      removed_lines = modification.source_code_before.splitlines()
      path = modification.old_path
  elif modification.change_type == ModificationType.ADD or \
      modification.change_type == ModificationType.MODIFY or \
      modification.change_type == ModificationType.RENAME:
      removed_lines = __get_lines_from_diff(modification.diff_parsed['deleted'])
      added_lines = __get_lines_from_diff(modification.diff_parsed['added'])
      path = modification.new_path
  else:
      raise Exception('Invalid Modification Type change')
  return (source_code, removed_lines, added_lines, path)

def __get_lines_from_diff(parsed_modifications):
    if parsed_modifications == None:
        return []

    return [ removed_line for _line_number, removed_line in parsed_modifications ]

