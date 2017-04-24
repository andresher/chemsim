import ply.yacc as yacc
import ChemSimTools as cst
from ChemSimLex import tokens

fluxes = []
machines = []
systems = []


def search_flux(name):
    for flux in fluxes:
        if flux.name == name:
            return flux


def search_machine(name):
    for machine in machines:
        if machine.name == name:
            return machine


def search_system(name):
    for system in systems:
        if system.name == name:
            return system


def p_statement(p):
    '''statement : create_flux
                 | create_machine
                 | create_system
                 | run
                 | save
                 | test'''
    p[0] = p[1]
    pass


def p_create_flux(p):
    '''create_flux : CREATE FLUX ID NUMBER compounds_list
                    | CREATE FLUX ID UNKNOWN compounds_list'''
    if isinstance(p[4], float):
        p[0] = cst.Flux(p[3], p[4])
    else:
        p[0] = cst.Flux(p[3], None)
    for name, percent in zip(*[iter(p[5])] * 2):
        p[0].add_compound({'name': name, '%': percent})
    fluxes.append(p[0])


def p_create_machine(p):
    'create_machine : CREATE MACHINE ID INPUT fluxes_list OUTPUT fluxes_list'
    p[0] = cst.Machine(p[3])
    for flux in p[5]:
        f = search_flux(flux)
        p[0].add_flux_in(f)
    for flux in p[7]:
        f = search_flux(flux)
        p[0].add_flux_out(f)
    machines.append(p[0])


def p_create_system(p):
    'create_system : CREATE SYSTEM ID machines_list'
    p[0] = cst.System(p[3])
    for machine in p[4]:
        m = search_machine(machine)
        p[0].add_machine(m)
    systems.append(p[0])


def p_compounds_list(p):
    '''compounds_list : ID NUMBER
                    | compounds_list ID NUMBER'''
    p[0] = []
    if len(p) > 3:
        p[0] = p[1]
        p[0].append(p[2])
        p[0].append(p[3])
    else:
        p[0] = [p[1], p[2]]


def p_fluxes_list(p):
    '''fluxes_list : ID
                | fluxes_list ID'''
    p[0] = []
    if len(p) > 2:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]



def p_machines_list(p):
    '''machines_list : ID
                    | machines_list ID'''
    p[0] = []
    if len(p) > 2:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]


def p_run(p):
    'run : RUN ID'
    system = search_system(p[2])
    system.solve()


def p_save(p):
    'save : SAVE ID'
    system = search_system(p[2])
    # TODO Save all the info of 'system'(above) into a CSV file.

def p_test(p):
    'test : TEST'
    for flux in fluxes:
        print("\nFlux Name:", flux.name)
        print("Speed:", flux.speed)
        for compound in flux.compounds:
            print("Compound:", compound['name'], "-", compound['%'])
    for machine in machines:
        print("\nMachine Name:", machine.name)
        for flux in machine.fluxes_in:
            print("Input Flux:", flux.name)
        for flux in machine.fluxes_out:
            print("Output Flux:", flux.name)
    for system in systems:
        print("\nSystem Name:", system.name)
        for machine in system.machines:
            print("Machine Name:", machine.name)

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()