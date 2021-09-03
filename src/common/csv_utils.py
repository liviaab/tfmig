import os
import csv
import shutil

def create_folder(folder_name):
  if not os.path.exists(folder_name):
    os.makedirs(folder_name)

  return

def create_csv(full_path, columns, lines, extrasaction='ignore'):
  with open(full_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=columns, extrasaction=extrasaction)
    writer.writeheader()

    for line in lines:
      writer.writerow(line)

  return

def remove_folder(path):
  if os.path.exists(path) and os.path.isdir(path):
    shutil.rmtree(path)
  return
