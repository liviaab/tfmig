import os
import shutil
import zipfile
import requests
from datetime import datetime
from git import Repo

def is_remote_repo(repo_url):
  return repo_url.startswith('http') 

def clone_repo(path):
  org = path.split('/')[-2]
  name = path.split('/')[-1]
  current_dir = os.getcwd()

  repo_path = current_dir + '/' + name
  repo = Repo.clone_from(path, repo_path)

  print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "OK")
  return repo_path

def remove_cloned_repo(path):
  print("{} - Removing repository...".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

  if os.path.exists(path) and os.path.isdir(path):
    shutil.rmtree(path)
  return
