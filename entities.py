from random import choice, random

from amak import AgentEntity, EnvironmentEntity

# Base class for all animals in the system
class Animal(AgentEntity):
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


# The Sheep can eat grass and reproduce
# self.amas.environment.eat_grass(self.on_grid_position) returns True if the Sheep ate grass
# Sheep(self.amas, self.on_grid_position) creates a new Sheep in the same position
# self.move_randomly() moves the Sheep in a random direction
# self.die() kills the Sheep
class Sheep(Animal):
    def __init__(self, mas, on_grid_position):
        super().__init__(mas, on_grid_position, "white")

    def on_act(self):
        # Exercise: Implement the Sheep behavior
        pass


# The Wolf can eat Sheep and reproduce
# self.amas.environment.get_prey(self.on_grid_position) returns the Sheep in the same position as the Wolf
# self.amas.environment.eat_prey(prey) kills the Sheep
# Wolf(self.amas, self.on_grid_position) creates a new Wolf in the same position
# self.move_randomly() moves the Wolf in a random direction
# self.die() kills the Wolf
class Wolf(Animal):
    def __init__(self, mas, on_grid_position):
        super().__init__(mas, on_grid_position, "red")

    def on_act(self):
        # Exercise: Implement the Wolf behavior
        pass



# The Grass can be eaten by Sheep
class GrassEntity(EnvironmentEntity):
    def __init__(self, initial_position):
        super().__init__(initial_position, "green")
        self.value = 100

    def eat(self):
        ate = self.value >= 100
        self.value = 0
        self.set_color((0, 255 * self.value / 100, 0))
        return ate

    def grow(self):
        self.value += 0.1
        if self.value > 100:
            self.value = 100
        self.set_color((0, 255 * self.value / 100, 0))