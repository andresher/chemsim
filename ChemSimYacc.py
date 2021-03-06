import ply.yacc as yacc
import ChemSimTools as cst
import csv
from ChemSimLex import tokens

fluxes = []
machines = []
systems = []

def name_in_use(name):
    for flux in fluxes:
        if flux.name == name:
            return True
    for machine in machines:
        if machine.name == name:
            return True
    for system in systems:
        if system.name == name:
            return True
    return False

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
    try:
        if name_in_use(p[3]):
            print("Unable to create flux, name already in use.")
            return
        if isinstance(p[4], float):
            p[0] = cst.Flux(p[3], p[4])
        else:
            p[0] = cst.Flux(p[3], None)
        percentage = 0.0
        for name, percent in zip(*[iter(p[5])] * 2):
            p[0].add_compound({'name': name, '%': percent})
            percentage += percent
        if percentage != 100:
            print("Unable to create flux, percentages do not add up to 100%.")
            return
        fluxes.append(p[0])

        print("Flux created successfully! [Name: %s, Speed: %s, Compounds:" % (p[0].name, p[0].speed), end="")
        for compound in p[0].compounds:
            print(" %s(%d%%)" % (compound['name'], compound['%']), end="")
        print("]")
    except:
        print("Error in definition, cannot create flux.")

def p_create_machine(p):
    'create_machine : CREATE MACHINE ID INPUT fluxes_list OUTPUT fluxes_list'
    try:
        if name_in_use(p[3]):
            print("Unable to create machine, name already in use.")
            return
        p[0] = cst.Machine(p[3])
        for flux in p[5]:
            f = search_flux(flux)
            p[0].add_flux_in(f)
        for flux in p[7]:
            f = search_flux(flux)
            p[0].add_flux_out(f)
        machines.append(p[0])
        p[0].fluxes_in[0].name # Trigger an exception before print, if necessary
        print("Machine created successfully! [Name: %s, Input Fluxes:" % p[0].name, end="")
        for flux in p[0].fluxes_in:
            print(" %s" % flux.name, end="")
        print(", Output Fluxes:", end="")
        for flux in p[0].fluxes_out:
            print(" %s" % flux.name, end="")
        print("]")
    except:
        print("Error in definition, cannot create machine.")

def p_create_system(p):
    'create_system : CREATE SYSTEM ID machines_list'
    try:
        if name_in_use(p[3]):
            print("Unable to create system, name already in use.")
            return
        p[0] = cst.System(p[3])
        for machine in p[4]:
            m = search_machine(machine)
            p[0].add_machine(m)
        systems.append(p[0])

        print("System created successfully! [Name: %s, Machines:" % p[0].name, end="")
        for machine in p[0].machines:
            print(" %s" % machine.name, end="")
        print("]")
    except:
        print("Error in definition, cannot create system.")

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
    try:
        system = search_system(p[2])
        isSolved = system.solve()

        if isSolved:
            print("System solved successfully!")
        else:
            print("System cannot be solved.")
    except:
        print("System was not defined correctly, cannot run.")

def p_save(p):
    'save : SAVE ID'
    try:
        system = search_system(p[2])
        isSolved = system.solve()

        if isSolved:

            file_name = system.name
            with open(file_name+'.csv', 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(['Machine Name', 'Flux Name', 'Speed', 'Compounds'])
                for machine in system.machines:

                    for flux in machine.all_fluxes:
                        row=[machine.name, flux.name, flux.speed]
                        compounds = ""
                        for compound in flux.compounds:
                            compounds += str(compound['name']) + "(" + str(compound['%'])+"%) "
                        row.append(compounds)
                        spamwriter.writerow(row)

                    print("System saved successfully as " + file_name + ".csv!")
        else:
            print("System cannot be solved and will not be saved.")
    except:
        print("System was not defined correctly, cannot save.")

def p_test(p):
    'test : TEST'

    for flux in fluxes:
        print("Flux Name: %s, Speed: %s, Compounds:" % (flux.name, flux.speed), end="")
        for compound in flux.compounds:
            print(" %s(%d%%)" % (compound['name'], compound['%']), end="")
        print("")

    for machine in machines:
        print("Machine Name: %s, Input Fluxes:" % machine.name, end="")
        for flux in machine.fluxes_in:
            print(" %s" % flux.name, end="")
        print(", Output Fluxes:", end="")
        for flux in machine.fluxes_out:
            print(" %s" % flux.name, end="")
        print("")

    for system in systems:
        print("System Name: %s, Machines:" % system.name, end="")
        for machine in system.machines:
            print(" %s" % machine.name, end="")
        print("")

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()
