import os
import shutil
import zipfile
import requests
from datetime import datetime

def is_remote_repo(repo_url):
  return repo_url.startswith('http') 

def clone_repo(path):
  base_url = "https://api.github.com"
  default_headers = {
      "Accept": "application/vnd.github.v3+json"
    }
  print("{} - Cloning repository...".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
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
  print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "OK")
  return filepath

def remove_cloned_repo(path):
  print("{} - Removing repository...".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
  if os.path.exists(path) and os.path.isdir(path):
    shutil.rmtree(path)
  return
