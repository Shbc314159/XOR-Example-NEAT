class globalvars():
    def __init__(self):
        self.barriers = []
        self.barriers_vertices = []
        self.x = -22
        self.z = -15

        self.target_vertices = (
            (self.x + 5, -9.5, self.z + 5),
            (self.x, -9.5, self.z + 5),
            (self.x, -9.5, self.z),
            (self.x + 5, -9.5, self.z),
        )

    def set_target_vertices(self, x, z):
        self.x = x
        self.z = z
        self.target_vertices = (
            (self.x + 5, -9.5, self.z + 5),
            (self.x, -9.5, self.z + 5),
            (self.x, -9.5, self.z),
            (self.x + 5, -9.5, self.z),
        )
        
globalvars = globalvars()