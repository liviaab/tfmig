from src.common.input_parser import *
from src.releases_analyzer import run as analyze_releases
from src.delta_analyzer.main import run as analyze_delta
from src.code_transformation.main import run as code_transformation

def main(argv):
  (script, input_arg) = parse_line_command(argv)

  if script == DELTA_COMMITS_SCRIPT:
    urls = urls_from_input(input_arg)
    analyze_delta(urls)

  elif script == RELEASES_SCRIPT:
    analyze_releases(input_arg)
  
  elif script == CODE_TRANSFORMATION:
    code_transformation()

if __name__ == "__main__":
  main(sys.argv[1:])
