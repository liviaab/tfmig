from src.common.columns import *

author_columns = [
  "email",
  "total_commits",
  "migration_contributor",
  "migration_commits"
]

def handle_authors_info(all_commits):
  authors_info_by_email = {}
  authors_info_by_name = {}

  for commit in all_commits:
    current_author_email = commit["author_email"]
    if current_author_email not in authors_info_by_email:
      authors_info_by_email[current_author_email] = {
        "email": current_author_email,
        "total_commits": 1,
        "migration_contributor": commit["are_we_interested"],
        "migration_commits": 1 if commit["are_we_interested"] else 0
      }
    else:
      authors_info_by_email[current_author_email]["total_commits"] += 1
      authors_info_by_email[current_author_email]["migration_contributor"] |= commit["are_we_interested"]
      authors_info_by_email[current_author_email]["migration_commits"] += 1 if commit["are_we_interested"] else 0

    current_author_name = commit["author_name"]
    if current_author_name not in authors_info_by_name:
      authors_info_by_name[current_author_name] = {
        "email": current_author_name,
        "total_commits": 1,
        "migration_contributor": commit["are_we_interested"],
        "migration_commits": 1 if commit["are_we_interested"] else 0
      }
    else:
      authors_info_by_name[current_author_name]["total_commits"] += 1
      authors_info_by_name[current_author_name]["migration_contributor"] |= commit["are_we_interested"]
      authors_info_by_name[current_author_name]["migration_commits"] += 1 if commit["are_we_interested"] else 0

    
  return (
    __format(authors_info_by_name),
    __format(authors_info_by_email)
  )


def __format(authors_dict):
  authors = [ value for _key, value in authors_dict.items() ]
  return authors
