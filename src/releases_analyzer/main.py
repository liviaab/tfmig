import os
from datetime import datetime
from src.common import read_csv, create_csv, apis_columns
from src.releases_analyzer.process_checkouts import analyze_checkouts

def run(input_folder):
  for root, dirs, files in os.walk(input_folder):
    for file in files:
      if file.startswith("release_commits_"):
        filepath = os.path.join(root, file)

        print("Proccessing {}".format(file))
        commits = read_csv(filepath)
        repo_url = commits[0]["repo_url"] + '/'
        selected_hashes = [ commit["hash"] for commit in commits ]
        # Clone the repo and visit each checkout to get test information through time
        apis_info = analyze_checkouts(repo_url, selected_hashes)
        
        print("Creating csv with APIs information - {}\n".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        file_name = file.replace("release_commits_", "release_info_")
        report_path = os.path.join(root, file_name)
        create_csv(report_path, apis_columns, apis_info)
  
  print("Done!")
  return
