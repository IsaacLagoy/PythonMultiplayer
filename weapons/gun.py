from weapons.bullet import Bullet
from basilisk import Node
import glm
import random


class Gun():
    
    def __init__(self, game, count: int, capacity: int, cooldown: float, spread: float, ricochets: int, damage: int, radius: float, color: str, owner: str='enemy') -> None:
        self.game = game
        self.count = count
        self.capacity = capacity
        self.cooldown = cooldown
        self.spread = spread
        
        self.ricochets = ricochets
        self.damage = damage
        self.radius = radius
        self.color = color
        self.owner = owner
        
        self.time = cooldown
        
    def get_bullet(self, position: glm.vec3, path: glm.vec3) -> Bullet:
        if self.color == 'black':
            cylinder = Node(
                position, 
                scale = (self.radius, 0.01, self.radius),
                mesh = self.game.cylinder_mesh
            )
            self.game.dimension_scene.add(cylinder)
            return Bullet(self.ricochets, self.damage, self.radius, self.color, cylinder, glm.vec3(path), glm.vec3(position), self.owner)
        else: return Bullet(self.ricochets, self.damage, self.radius, self.color, None, glm.vec3(path), glm.vec3(position), self.owner)
        
    def update(self, dt: float) -> None:
        """
        Updates cooldown timer
        """
        self.time += dt
    
    def shoot(self, position: glm.vec3, forward: glm.vec3) -> list:
        """
        Returns a list of fired bullets if the gun is shot
        """
        if self.time < self.cooldown: return
        self.time = 0
        
        bullets = []
        for _ in range(self.count):
            path = glm.normalize(forward + [random.uniform(-self.spread, self.spread) for _ in range(3)])
            bullets.append(self.get_bullet(position, path))
            
        self.game.shot.play()
            
        return bullets
    
    def __repr__(self) -> str:
        return f'Gun - bullets: {self.count}, capacity: {self.capacity}, cooldown: {self.cooldown}, spread: {self.spread}'