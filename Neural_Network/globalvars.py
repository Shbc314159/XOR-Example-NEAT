class globalvars():
    def __init__(self):
        self.barriers = []
        self.barriers_vertices = []
        self.x = 25
        self.z = -15

        self.target_vertices = (
            (self.x + 5, -9.5, self.z + 5),
            (self.x, -9.5, self.z + 5),
            (self.x, -9.5, self.z),
            (self.x + 5, -9.5, self.z),
        )

        self.back_wall_vertices = (
            (75, -10, -60),
            (25, -10, -60), 
            (25, 20, -60),
            (75, 20, -60),
        )


        self.back_wall_surface = (
            (0, 1, 2, 3) 
        )
        
        self.floor_vertices = (
            (75, -10, -10),
            (25, -10, -10),
            (25, -10, -60),
            (75, -10, -60),   
        )

        self.floor_surface = (
            (0, 1, 2, 3)
        )
         
        self.target_surface = (
            (0, 1, 2, 3)
        )

        self.cube_start = [50, -9, -55]

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