import ply.lex as lex

# Reserved words
reserved = {
    'create' : 'CREATE',
    'system' : 'SYSTEM',
    'flux' : 'FLUX',
    'machine' : 'MACHINE',
    'save' : 'SAVE',
    'run' : 'RUN',
    'name' : 'NAME',
    'fluxes' : 'FLUXES',
    'machines' : 'MACHINES',
    'member' : 'MEMBER',
    'input' : 'INPUT',
    'output' : 'OUTPUT',
    'speed' : 'SPEED',
    'compound' : 'COMPOUND',
}

# List of token names. This is always required
tokens = [
    'NUMBER',
    'UNKNOWN',
    'ID'
] + list(reserved.values())

# Regular expression rules for simple token
t_UNKNOWN = r'\?'

# Define number as int
def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
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