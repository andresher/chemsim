class Flux:
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed
        self.compounds = []

    def add_compound(self, compound):
        self.compounds.append(compound)

    def set_speed(self, speed):
        self.speed = speed


class Machine:

    def __init__(self, name):
        self.name = name
        self.fluxes_in = []
        self.fluxes_out = []
        self.all_fluxes = []

    def add_flux_in(self, flux):
        self.fluxes_in.append(flux)
        self.all_fluxes.append(flux)

    def add_flux_out(self, flux):
        self.fluxes_out.append(flux)
        self.all_fluxes.append(flux)



class System:

    def __init__(self, name):
        self.name = name
        self.machines = []

    def add_machine(self, machine):
        self.machines.append(machine)

    # Pre:      Every flux has list of compounds with percentages.
    #           Will only solve for unknown speeds of fluxes
    # Output:   False if it is not solvable
    #           True if the system was solved (unknown values will be populated in objects)
    def solve(self):
        # Flags
        isSolvable = True
        isSolved = False

        while(isSolvable and not isSolved):
            # Start thinking it is solved, and it is not solvable
            isSolved = True
            isSolvable = False

            for machine in self.machines:
                in_total = 0
                out_total = 0
                unknownCount = 0
                unknown = None
                for flux in machine.all_fluxes:
                    #Count speeds in
                    if(flux in machine.fluxes_in and flux.speed != None):
                        in_total = in_total + flux.speed

                    #Count speeds out
                    if(flux in machine.fluxes_out and flux.speed != None):
                        out_total = out_total + flux.speed

                    #Count unknowns
                    if(flux.speed == None):
                        isSolved = False # If any unknown is found, it is not solved
                        unknownCount = unknownCount + 1
                        unknown = flux
                if(unknownCount == 1):
                    unknown.speed = abs(in_total-out_total)
                    isSolvable = True # If you have a machine with only one unknown it is still solvable
        return isSolved