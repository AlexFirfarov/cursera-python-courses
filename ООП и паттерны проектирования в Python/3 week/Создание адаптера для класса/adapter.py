class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def lighten(self, grid):
        self.adaptee.set_dim((len(grid[0]), len(grid)))
        lights = []
        obstacles = []
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                if grid[i][j] == 1:
                    lights.append((j, i))
                elif grid[i][j] == -1:
                    obstacles.append((j, i))
        self.adaptee.set_obstacles(obstacles)
        self.adaptee.set_lights(lights)
        return self.adaptee.generate_lights()
