import os
import shutil
import zipfile
import requests

from src.heuristics import UnittestRef, PytestRef
from src.common.extensions import *
from src.common.search_patterns import *

VALID_EXTENSIONS = [PYTHON_EXTENSION] + CI_OR_CONFIG_EXTENSIONS 

def analyze_current(path):
  if __is_remote_repo(path):
    path = __clone_repo(path)
    total_files, unittest_files, pytest_files, both_files = __examine_local_repo(path)
    __remove_cloned_repo(path)
  else:
    total_files, unittest_files, pytest_files, both_files = __examine_local_repo(path)

  return ( total_files, unittest_files,  pytest_files, both_files ) 


def __is_remote_repo(repo_url):
  return repo_url.startswith('http') 

def __clone_repo(path):
  base_url = "https://api.github.com"
  default_headers = {
      "Accept": "application/vnd.github.v3+json"
    }
  response = requests.get(
              self.base_url + "/repos/{}/{}/zipball".format(org, name),
              headers=final_headers,
              stream=True
            )

  if response.status_code != 200:
    raise Exception("Failed to query Github API. Response status {}".format(response.status_code))
  
  # write blob 
  zip_path = "{}-{}.zip".format(org, name)
  with open(zip_path, "wb") as fd:
    for chunk in response.iter_content(chunk_size=512):
      fd.write(chunk)
  
  # extract blob
  filepath = "{}-{}".format(org, name)
  with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(filepath)

  os.remove(zip_path)
  return filepath

def __remove_cloned_repo(path):
  if os.path.exists(path) and os.path.isdir(path):
    shutil.rmtree(path)
  return

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

  return (total_files, unittest_files, pytest_files, both_files)

def __search_patterns_in_content(patterns, content):
  result = search_patterns_in_content(patterns, content)
  key = next( key for key in list(result.keys()) if key.startswith('count_') )
  return result[key] > 0
