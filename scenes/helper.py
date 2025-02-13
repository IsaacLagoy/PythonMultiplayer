import glm
from basilisk import Node
import random

    
def rect_room(centerx, centerz, width, depth, height, game) -> list[Node]:
    nodes = [Node(
        position = (data[0], -1 + height, data[1]), 
        scale = (data[2], height, data[3]),
        collision = True,
        material = random.choice(game.materials)
    ) for data in (
        (centerx + width, centerz, 1, depth), 
        (centerx - width, centerz, 1, depth), 
        (centerx, centerz + depth, width, 1), 
        (centerx, centerz - depth, width, 1)
    )]
    
    nodes += [Node(
        scale = (width, 1, depth),
        collision = True,
        position=(centerx, y, centerz),
        material = random.choice(game.materials)
    ) for y in (-1, height * 2)]
    return nodes