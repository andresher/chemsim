import ply.lex as lex

# Reserved words
reserved = {
    'create': 'CREATE',
    'system': 'SYSTEM',
    'flux': 'FLUX',
    'machine': 'MACHINE',
    'save': 'SAVE',
    'run': 'RUN',
    'name': 'NAME',
    'machines': 'MACHINES',
    'input': 'INPUT',
    'output': 'OUTPUT',
    'speed': 'SPEED',
    'compounds': 'COMPOUNDS',
    'test': 'TEST',
}

# List of token names. This is always required
tokens = [
    'NUMBER',
    'UNKNOWN',
    'ID'
] + list(reserved.values())

# Regular expression rules for simple token
t_UNKNOWN = r'\?'

# Define number as float
def t_NUMBER(t):
    r'(\d+(\.\d*)?|\.\d+)'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Not a valid float %d", t.value)
        t.value = 0
    return t

# Define a rule for reserved words
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()