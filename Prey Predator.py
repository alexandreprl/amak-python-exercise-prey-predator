from random import random, choice

import amak.amakpygame
from amak import AMAKPygame

GRID_WIDTH = 100
GRID_HEIGHT = 100


class PreyPredatorMAS(amak.MAS):
    def __init__(self, environment):
        super().__init__(environment)


class GrassEntity(amak.EnvironmentEntity):
    def __init__(self, initial_position):
        super().__init__(initial_position, "green")
        self.value = 100

    def eat(self):
        ate = self.value >= 100
        self.value = 0
        self.set_color((0, 255 * self.value / 100, 0))
        return ate

    def grow(self):
        self.value += 1
        if self.value > 100:
            self.value = 100
        self.set_color((0, 255 * self.value / 100, 0))


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

    def eat(self, on_grid_position):
        self.grass[on_grid_position[1]][on_grid_position[0]].eat()

    def get_prey(self, on_grid_position):
        res = self.grid[on_grid_position[1]][on_grid_position[0]]
        # find object of type Prey in res array
        for y in range(len(res)):
            if isinstance(res[y], Prey):
                return res[y]
        return None

    def eat_prey(self, prey):
        on_grid_position = prey.on_grid_position
        res = self.grid[on_grid_position[1]][on_grid_position[0]]
        for x in range(len(res)):
            if isinstance(res[x], Prey):
                res[x].die()
                return

    def render(self, display_surface):
        for y in range(len(self.grass)):
            for x in range(len(self.grass[y])):
                if self.grass[y][x]:
                    display_surface.blit(self.grass[y][x].surface, self.grass[y][x].rect)


environment = PreyPredatorEnvironment()
mas = PreyPredatorMAS(environment)


class Animal(amak.AgentEntity):
    def __init__(self, mas, on_grid_position, color):
        self.on_grid_position = on_grid_position
        super().__init__(mas, self.grid_to_display_position(self.on_grid_position), color)

    def grid_to_display_position(self, on_grid_position):
        return 5 + on_grid_position[0] * 10, 5 + on_grid_position[1] * 10

    def set_grid_position(self, on_grid_position):
        g = self.amas.environment.grid[self.on_grid_position[1]][self.on_grid_position[0]]
        if self in g:
            g.remove(self)
        self.on_grid_position = on_grid_position
        self.set_position(self.grid_to_display_position(on_grid_position))
        self.amas.environment.grid[self.on_grid_position[1]][self.on_grid_position[0]].append(self)

    def move_randomly(self):
        new_position = None
        while not self.amas.environment.is_on_grid_position_valid(new_position):
            direction = choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            new_position = (self.on_grid_position[0] + direction[0], self.on_grid_position[1] + direction[1])
        self.set_grid_position(new_position)

    def die(self):
        self.destroy()
        self.amas.environment.grid[self.on_grid_position[1]][self.on_grid_position[0]].remove(self)


class Prey(Animal):
    def __init__(self, mas, on_grid_position):
        self.life = 100
        super().__init__(mas, on_grid_position, "white")

    def on_act(self):
        if self.amas.environment.eat(self.on_grid_position):
            self.life += 10
        else:
            self.life -= 1
        if self.life <= 0:
            self.die()
        else:
            if random() < 0.01:
                Prey(mas, self.on_grid_position)
            else:
                self.move_randomly()


class Predator(Animal):
    def __init__(self, mas, on_grid_position):
        self.life = 100
        super().__init__(mas, on_grid_position, "red")

    def on_act(self):
        prey = self.amas.environment.get_prey(self.on_grid_position)
        if prey is not None:
            self.amas.environment.eat_prey(prey)
            self.life += 10
        else:
            self.life -= 1
        if self.life <= 0:
            self.die()
        else:
            if random() < 0.01:
                Predator(mas, self.on_grid_position)
            else:
                self.move_randomly()


for i in range(20):
    x = int(random() * GRID_WIDTH)
    y = int(random() * GRID_HEIGHT)
    Prey(mas, (x, y))
for i in range(20):
    x = int(random() * GRID_WIDTH)
    y = int(random() * GRID_HEIGHT)
    Predator(mas, (x, y))

if __name__ == "__main__":
    AMAKPygame(mas, environment, GRID_WIDTH * 10, GRID_HEIGHT * 10, 120)
