import os
import re
from datetime import datetime

from src.code_transformation.transformation import run as analyze_transformation
from src.code_transformation.columns import *
from src.common import *

migrated_dir = './migrated/'
ongoing_dir = './ongoing/'
# folders = [migrated_dir]
folders = [migrated_dir, ongoing_dir]

def run():
  output_folder = "out_t_" + datetime.now().strftime("%m-%d-%Y_%H%M%S")
  create_folder(output_folder)
  previous_results = __init_aggregated_results()

  for folder in folders:
    for filename in __list_files(folder):
      file_path = os.path.join(folder, filename)
      results = analyze_transformation(file_path)

      filename = re.sub(r'[.|\/]', "", folder) + "_" + os.path.splitext(filename)[0] + "_" + "transformations.csv"
      file_path = os.path.join(output_folder, filename)
      # creates intermediate csv
      create_csv(file_path, output_columns, results)
      previous_results = __aggregate_results(previous_results, results)

    # creates aggregated csv
    filename = re.sub(r'[.|\/]', "", folder) + "_" + "aggregated.csv"
    file_path = os.path.join(output_folder, filename)
    create_csv(file_path, output_columns, previous_results)

  return

def __list_files(folder):
  return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

def __init_aggregated_results():
  results = []
  for transformation_type in list(transformation_columns_by_type.keys()):
    results.append(__init_type_result(transformation_type))

  return results

def __init_type_result(transformation_type):
  result = {}
  for column in output_columns:
    result[column] = 0

  result["Transformation type"] = transformation_type
  return result

def __aggregate_results(previous_results, new_results):
  # print("previous_results", previous_results)
  # print("new_results", new_results)
  result = []
  for new_values in new_results:
    old_values = __find_old_values(previous_results, new_values["Transformation type"])
    tmp = {}
    for key, value in new_values.items():
      # print(key)
      if key == "Transformation type":
        tmp[key] = new_values["Transformation type"]
      else:
        tmp[key] = old_values[key] + new_values[key]
    result.append(tmp)

  return result

def  __find_old_values(old_results, transformation_type):
  for value in old_results:
    if value["Transformation type"] == transformation_type:
      return value

  return None
