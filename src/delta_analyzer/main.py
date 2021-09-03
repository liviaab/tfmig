import os
from datetime import datetime

from src.current_analyzer import *
from src.delta_analyzer.repo_analyzer import *
from src.common import *

def run(paths):
  output_folder = "out" + datetime.now().strftime("%m-%d-%Y_%H%M%S")
  create_folder(output_folder)
  aggregated_metrics = []

  for path in paths:
    project_name = path.split('/')[-1]
    print("Analyzing delta commits {}...".format(project_name))
    (
      framework_occurrences,
      migration_occurrences,
      allcommits,
      authors_info_by_name,
      authors_info_by_email
    ) = analyze_commits(path)

    print("Analyzed {} commits.".format(len(allcommits)))
    
    print("Cloning Repo and checking current state... {}.".format(datetime.now().strftime("%m-%d-%Y_%H%M%S")))
    aggregated_metrics.append(
      extract_metadata(framework_occurrences, migration_occurrences, allcommits, authors_info_by_name, authors_info_by_email)
    )

    print("Generating csvs")
    author_path = os.path.join(output_folder, "authors_"+project_name+'.csv')
    commits_path = os.path.join(output_folder, "commits_"+project_name+'.csv')
    release_path = os.path.join(output_folder, "release_commits_"+project_name+'.csv')

    create_csv(author_path, author_columns, authors_info_by_email)
    create_csv(commits_path, commit_columns, allcommits)
    create_csv(release_path, ["index", "repo_url", "hash"], __extract_sample_commit_hashes(allcommits))
    print("")

  metrics_path = os.path.join(output_folder, "000_metrics.csv")
  create_csv(metrics_path, repositories_columns, aggregated_metrics)

  return metrics_path

STEP = 5
def __extract_sample_commit_hashes(allcommits):
  release_hashes = \
    [ {"hash": commit["commit_hash"], "index": commit["commit_index"], "repo_url": commit["repo_url"]} \
      for commit in allcommits if commit["commit_index"] % STEP == 0 ]
  return release_hashes

