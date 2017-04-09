class System:

    def __init__(self, name):
        self.name = name
        self.fluxes = {}
        self.machines = {}

    def get_name(self):
        return self.name

    def get_fluxes(self):
        return self.fluxes

    def get_machines(self):
        return self.machines

    def add_flux(self, flux):
        self.fluxes.append(flux)

    def add_machine(self, machine):
        self.machines.append(machine)

class Machine:

    def __init__(self, machine_in, machine_out):
        self.machine_in = machine_in
        self.machine_out = machine_out


class Flux:

    def __init__(self, machine_in, machine_out, speed, compounds):
        self.machine_in = machine_in
        self.machine_out = machine_out
        self.speed = speed
        self.compounds = compounds
