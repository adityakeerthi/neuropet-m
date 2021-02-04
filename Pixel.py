class Pixel:
    def __init__(self, tracers, position):
        self.tracers = tracers
        self.dimensions = len(tracers)
        self.x = position["x"]
        self.y = position["y"]
        self.z = position["z"]
        self.concentration = {}
        for tracer in tracers:
            self.concentration[tracer] = 0.0
    
    def RGB_to_Concentration(self, rgb):
        return rgb

    def Add_Concentration(self, tracer, rgb):
        return tracer