"""
1. Double quoted
2. It can contain any backslash-escaped character
3. It can contain any character except double quote
"""
STRING_LITERAL_REGEX = r'\"(\\.|[^"])*\"' 

"""
^        // Match at the beginning
[_a-z]   // Match special character _$%& or "a-z" at the beginning 
\\w*     // Match zero or more of characters - [a-zA-Z0-9_], after the beginning
$        // Till the end
"""
VARIABLE_NAME_REGEX = r'^[a-zA-Z_$&%][\w_$&%]*$'