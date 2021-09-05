import os

from src.heuristics import UnittestRef, PytestRef
from src.common.extensions import VALID_EXTENSIONS
from src.common.search_patterns import *
from src.common.remote_repo import *

def analyze_current(path):
  if is_remote_repo(path):
    path = clone_repo(path)
    total_files, unittest_files, pytest_files, both_files = __examine_local_repo(path)
    remove_cloned_repo(path)
  else:
    total_files, unittest_files, pytest_files, both_files = __examine_local_repo(path)

  return ( total_files, unittest_files,  pytest_files, both_files ) 

def __examine_local_repo(local_path):
  total_files = 0
  unittest_files = 0
  pytest_files = 0
  both_files = 0

  walk_dir = os.path.abspath(local_path)
  excluded_folders = ['.git']

  for currentpath, folders, files in os.walk(walk_dir, topdown=True):
    folders[:] = [ f for f in folders if f not in excluded_folders ]

    for file in files:
      total_files += 1
      _name, extension = os.path.splitext(file)
      if extension not in VALID_EXTENSIONS:
        continue

      usesUnittest = False
      usesPytest = False

      with open(os.path.join(currentpath, file), 'r') as src:
        try:
          content = src.read()
          if __search_patterns_in_content(UnittestRef, content):
            usesUnittest = True
            unittest_files += 1

          if __search_patterns_in_content(PytestRef, content):
            usesPytest = True
            pytest_files +=1

          if usesUnittest and usesPytest:
            both_files += 1
        except:
          print("Something went wrong at {}".format(os.path.join(currentpath, file)))
          continue

  return (total_files, unittest_files, pytest_files, both_files)

def __search_patterns_in_content(patterns, content):
  result = search_patterns_in_content(patterns, content)
  key = next( key for key in list(result.keys()) if key.startswith('count_') )
  return result[key] > 0
