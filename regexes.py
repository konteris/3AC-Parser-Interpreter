import re

"""
1. Double quoted
2. It can contain any backslash-escaped character
3. It can contain any character except double quote
"""
STRING_LITERAL_REGEX = r'\"(\\.|[^"])*\"' 