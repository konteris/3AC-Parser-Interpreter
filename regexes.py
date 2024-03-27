"""
\"       Match double quote
\\.      Match any backslash-escaped character except newline
|        OR
[^"]*    Match any character except double quote, zero or more times
\"       Match double quote
"""

STRING_LITERAL_REGEX = r'\"(\\.|[^"])*\"'

"""
^        Match at the beginning
[_a-z]   Match special character _$%& or "a-z" at the beginning 
\\w*     Match zero or more of characters - [a-zA-Z0-9_], after the beginning
$        Till the end
"""
VARIABLE_NAME_REGEX = r'^[a-zA-Z_$&%][\w_$&%]*$'

"""
^        Match at the beginning
[+-]?    Match optional + or - sign
[1-9]+   Match one or more of 1-9
[0-9]*   Match zero or more of 0-9
$        Till the end
"""
INTEGER_LITERAL_REGEX = r'^[+-]?(0|[1-9]+[0-9]*)$'

"""
        Same as variable name but starts with @
"""
LABEL_NAME_REGEX = r'^@[a-zA-Z_$&%][\w_$&%]*$'
