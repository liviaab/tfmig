import os
import shutil
from git import Repo

from src.delta_analyzer.tasks import is_test_file
from src.heuristics import *
from src.common import *

def analyze_checkouts(repo_url, selected_commits):
  if is_remote_repo(repo_url):
    local_path = clone_repo(repo_url)
    apis_info = __examine_local_repo(local_path, selected_commits)
    remove_cloned_repo(local_path)
  else:
    apis_info = __examine_local_repo(repo_url, selected_commits)

  return apis_info


def __examine_local_repo(local_path, commits):
  apis_info = []
  repo = Repo(local_path)

  for commit_hash in commits:
    repo.git.checkout(commit_hash)
    counts = { key: 0 for key in apis_columns if key.startswith('count_') }
    matches = { key: [] for key in apis_columns if key.startswith('matches_') }
    infos = { **counts, **matches }

    for path, _, files in os.walk(local_path):
      if '.git/' in path:
        continue

      for filename in files:
        _name, extension = os.path.splitext(filename)

        if extension not in VALID_EXTENSIONS:
          continue
        
        if is_test_file(filename):
          infos["count_test_files"] += 1

        with open(os.path.join(path,  filename), 'r') as src: 
          try:
            content = src.read()
            patterns = APIsUnittest + APIsPytest + TestMethodRef
            apis = search_patterns_in_content(patterns, content)

            for column in apis.keys():
              infos[column] = infos[column] + apis[column]

          except Exception as e:
            print("Reading Error - Skipping file", path + filename)
            print(e)
            continue

      infos["commit_hash"] = commit_hash
      apis_info.append(infos)
  
  # try to return to the current state
  try:
    repo.git.checkout('master')
  except git.GitCommandError:
    repo.git.checkout('main')
  except: 
    pass

  return apis_info
