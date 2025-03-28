from amak import MAS

from entities import GrassEntity, Sheep

GRID_WIDTH = 100
GRID_HEIGHT = 100


class PreyPredatorMAS(MAS):
    def __init__(self, environment):
        super().__init__(environment)



class PreyPredatorEnvironment:
    def __init__(self):
        w, h = GRID_WIDTH, GRID_HEIGHT
        self.grid = [[[] for x in range(w)] for y in range(h)]
        self.grass = [[GrassEntity((5 + 10 * x, 5 + 10 * y)) for x in range(w)] for y in range(h)]

    def is_on_grid_position_valid(self, position):
        if position is None:
            return False
        x, y = position
        return 0 <= position[0] < len(self.grid[0]) and 0 <= position[1] < len(self.grid)

    def cycle(self):
        for y in range(len(self.grass)):
            for x in range(len(self.grass[y])):
                if self.grass[y][x]:
                    self.grass[y][x].grow()

    def eat_grass(self, on_grid_position):
        return self.grass[on_grid_position[1]][on_grid_position[0]].eat()

    def get_grass(self, on_grid_position):
        return self.grass[on_grid_position[1]][on_grid_position[0]]

    def get_sheep(self, on_grid_position):
        res = self.grid[on_grid_position[1]][on_grid_position[0]]
        # find object of type Prey in res array
        for y in range(len(res)):
            if isinstance(res[y], Sheep):
                return res[y]
        return None

    def eat_sheep(self, on_grid_position):
        res = self.grid[on_grid_position[1]][on_grid_position[0]]
        for x in range(len(res)):
            if isinstance(res[x], Sheep):
                res[x].die()
                return

    def render(self, display_surface):
        for y in range(len(self.grass)):
            for x in range(len(self.grass[y])):
                if self.grass[y][x]:
                    display_surface.blit(self.grass[y][x].surface, self.grass[y][x].rect)

