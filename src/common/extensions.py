# Valid extensions to search for unittest and pytest patterns
# We need this to filter which files to analyze, otherwise
# it would take a lot more time to process and classify
PYTHON_EXTENSION = '.py'
CI_OR_CONFIG_EXTENSIONS = ['.yaml', '.yml', '.ini', '.toml', '.cfg', '.sh']

VALID_EXTENSIONS = [PYTHON_EXTENSION] + CI_OR_CONFIG_EXTENSIONS
