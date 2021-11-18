# from https://www.tutorialspoint.com/python3/python_command_line_arguments.htm
import sys
import getopt
import os

SCRIPT_USAGE = '\nUsage: \n\t main.py -s analyze_delta_commits -i <inputfile>.csv \nor \n\t main.py -s analyze_releases -i <inputfolder> \n\n'
DELTA_COMMITS_SCRIPT = "analyze_delta_commits"
RELEASES_SCRIPT = "analyze_releases"
CODE_TRANSFORMATION = "code_transformation"

def parse_line_command(argv):
  input_arg = ''

  try:
    opts, _args = getopt.getopt(argv, "hs:i:", ["script=", "input="])
  except getopt.GetoptError:
    print(SCRIPT_USAGE)
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      print(SCRIPT_USAGE)
      sys.exit()
    elif opt in ("-i", "--input"):
      input_arg = arg
    elif opt in ("-s", "--script"):
      script = arg

  if (not input_arg or not script) and not (script == CODE_TRANSFORMATION) :
    print(SCRIPT_USAGE)
    sys.exit()

  if script == DELTA_COMMITS_SCRIPT and (not input_arg.endswith('.csv') or not os.path.isfile(input_arg)):
    print(SCRIPT_USAGE)
    print('\tThe input argument must exist and it must be a .csv')
    sys.exit()
  
  if script == RELEASES_SCRIPT and not os.path.isdir(input_arg):
    print(SCRIPT_USAGE)
    print('\tThe input folder must exist')
    sys.exit()

  return (script, input_arg)


def urls_from_input(inputfile):
  urls = []

  with open(inputfile, 'r') as file:
    for line in file:
      values = line.rstrip().replace(' ', '').split(",")
      values = filter(lambda word: word != '', values)
      urls.extend(values)

  return urls
