from entities.enemy import Enemy
from basilisk import Node


class GameScene():

    def __init__(self) -> None:
        self.nodes: list[Node] = []
        self.enemies: list[Enemy] = []
        self.guns: list[tuple] = []
        
def get_plain_nodes(game_scene: GameScene) -> list[Node]:
    """
    Removes all nodes with physics bodies
    Removes all colliders from nodes
    Removes all enemies
    """
    nodes = [node.deep_copy() for node in game_scene.nodes]
    to_remove = []
    
    for node in nodes:
        if node.physics:
            to_remove.append(node)
            continue
            
        node.collision = False
        
    for node in to_remove: nodes.remove(node)
        
    return nodes