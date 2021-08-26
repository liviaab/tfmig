# Custom pattern to ignore docstrings
from pyparsing import QuotedString
docString = QuotedString(quoteChar='"""', multiline=True, unquoteResults=False)
