import ply.lex as lex

literals = ( '+','-','*','/','<','>','=','(',')','{','}','[',']',',',';' )

keywords = (
    'WHOLE', 'DECIMAL', 'WORD', 'FLAG', 
    'READ', 'WRITE', 'LOOP', 'WHEN', 'OTHERWISE',
    'FROM', 'TO', 'BY', 'ACTION', 'CALL'
)

tokens = keywords + (
    'INTEGER', 'FLOAT', 'STRING', 'BOOL', 'ID'
)

# Token regex patterns
# t_BOOL = r'TRUE'
t_INTEGER = r'\d+'
t_FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_STRING = r'`.*?`'
t_ignore_COMMENT = r'\#.*'

# ID

def t_ID(t):
    r'[A-Za-z][A-Za-z0-9]*'
    if t.value.upper() in keywords:
        t.type =t.value = t.value.upper()
    elif t.value.upper() in ['TRUE','FALSE']:
        t.type='BOOL'
        t.value=t.value.upper()
    return t


# Ignored characters
t_ignore = ' \t'

# Newline
def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex(debug=False,errorlog=None)