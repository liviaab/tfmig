import os
import csv
import math
from src.code_transformation.columns import *


def run(file_path):
  print(file_path)
  try: 
    with open(file_path, newline='') as csvfile:
      csvreader = csv.DictReader(csvfile)
      migration_commits = __filter_migration_commits(csvreader)
      results_by_transformation = __aggregate_code_transformations(migration_commits)
  except:
    with open(file_path, newline='') as csvfile:
      csvreader = csv.DictReader(csvfile,  delimiter=';')
      migration_commits = __filter_migration_commits(csvreader)
      results_by_transformation = __aggregate_code_transformations(migration_commits)
    
  formatted_results = __format_results(results_by_transformation)
  return formatted_results

def __filter_migration_commits(csvreader):
  migration_commits = []
  for row in csvreader:
    if row["are_we_interested"] == 'True':
      migration_commits.append(row)


  return migration_commits

def __aggregate_code_transformations(migration_commits):
  # positions
  migration_commits_count = len(migration_commits)
  first_quarter_pos = math.ceil( migration_commits_count / 4 ) - 1
  half_pos = math.ceil( migration_commits_count / 2 ) - 1
  third_quarter_pos = math.ceil( migration_commits_count * 3 / 4) - 1

  transformation_types = list(transformation_columns_by_type.keys())
  results_by_transformation = __init_results_by_transformation()

  for index, row in enumerate(migration_commits):
    for transformation_type in transformation_types:
      results_by_transformation[transformation_type]["Transformation type"] = transformation_type
      
      if row[transformation_type] == 'True':
        u_removal, p_addition = __get_row_transformation(row, transformation_type)
        if index + 1 <= migration_commits_count:
          results_by_transformation[transformation_type]["100% - commit count"] += 1
          results_by_transformation[transformation_type]["100% - code transformation"] += (p_addition - u_removal)
          results_by_transformation[transformation_type]["total unittest removals"] += u_removal
          results_by_transformation[transformation_type]["total pytest additions"] += p_addition
        
        if index <= third_quarter_pos:
          results_by_transformation[transformation_type]["75% - commit count"] += 1 
          results_by_transformation[transformation_type]["75% - code transformation"] += (p_addition - u_removal)
        
        if index <= half_pos:
          results_by_transformation[transformation_type]["50% - commit count"] += 1
          results_by_transformation[transformation_type]["50% - code transformation"] += (p_addition - u_removal)
        
        if index <= first_quarter_pos:
          results_by_transformation[transformation_type]["25% - commit count"] += 1
          results_by_transformation[transformation_type]["25% - code transformation"] += (p_addition - u_removal)
        
        if index == 0: 
          results_by_transformation[transformation_type]["First - commit count"] += 1
          results_by_transformation[transformation_type]["First - code transformation"] += (p_addition - u_removal)

  return results_by_transformation

"""
In the end, we'll have:
{
   "Mig: assert": {...},
   "Mig: fixture": {
      "Transformation type": 0,
      "First -  commit count": 0,
      ... other output_columns
   },
   ...
}
"""
def __init_results_by_transformation():
  results = {}
  for transformation_type in list(transformation_columns_by_type.keys()):
    results[transformation_type] = __init_type_result()
  return results

def __init_type_result():
  result = {}
  for column in output_columns:
    result[column] = 0
  return result

def __get_row_transformation(row, transformation_type):
  if row[transformation_type] == 'False':
    return 0, 0

  columns = transformation_columns_by_type[transformation_type]
  u_removal = 0
  p_addition = 0
  for column in columns["u_removal"]:
    u_removal += int(row[column])

  for column in columns["p_addition"]:
    p_addition += int(row[column])
  
  return u_removal, p_addition

"""
From
{
   "Mig: assert": {...},
   "Mig: fixture": {
      "Transformation type": 0,
      "First -  commit count": 0,
      ... other output_columns
   },
   ...
}

To 
[
  {
    "Transformation type": "Mig: assert",
    "First -  commit count": 0,
    ... other output_columns
  },
    {
    "Transformation type": "Mig: fixture",
    "First -  commit count": 0,
    ... other output_columns
  },
  ....
]
"""

def __format_results(results_by_transformation):
  return [ value for key, value in results_by_transformation.items()]

