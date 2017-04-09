import ply.yacc as yacc
import ChemSimTools
from ChemSimLex import tokens


def p_statement_create_system(p):
    'statement_create_system : CREATE SYSTEM'
    # TODO


def p_statement_create_flux(p):
    'statement_create_flux : CREATE FLUX'
    # TODO


def p_statement_create_machine(p):
    'statement_create_machine : CREATE MACHINE'
    # TODO

def p_statement_assign_name(p):
    'statement_assign_name : NAME ID'
    # TODO

def p_statement_assign_input(p):
    'statement_assign_input : INPUT ID'
    # TODO

def p_statement_assign_output(p):
    'statement_assign_output : OUTPUT ID'
    # TODO

def p_statement_assign_speed(p):
    'statement_assign_speed : SPEED ID'
    # TODO

def p_statement_assign_compound(p):
    'statement_assign_compound : COMPOUND ID'
    # TODO

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()