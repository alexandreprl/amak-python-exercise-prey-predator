from random import random

from amak import AMAKPygame

from entities import Sheep, Wolf
from system import PreyPredatorEnvironment, PreyPredatorMAS, GRID_WIDTH, GRID_HEIGHT

environment = PreyPredatorEnvironment()
mas = PreyPredatorMAS(environment)

for i in range(20):
    x = int(random() * GRID_WIDTH)
    y = int(random() * GRID_HEIGHT)
    Sheep(mas, (x, y))
for i in range(20):
    x = int(random() * GRID_WIDTH)
    y = int(random() * GRID_HEIGHT)
    Wolf(mas, (x, y))

if __name__ == "__main__":
    AMAKPygame(mas, environment, GRID_WIDTH * 10, GRID_HEIGHT * 10, 120)
