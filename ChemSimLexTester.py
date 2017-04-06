# Lex tester
import ChemSimLex as lex

while True:
    # Input from command line
    data = input('ChemSIM > ')

    # Give lexer input
    lex.lexer.input(data)

    # Tokenize
    for tok in lex.lexer:
        print(tok)